import logging
import sys
from contextlib import asynccontextmanager
from typing import Optional

import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import (
    CLASS_DESCRIPTIONS,
    CLASS_LABELS,
    CLASS_RISK_LEVEL,
    RISK_DISPLAY,
    RISK_RECOMMENDATIONS,
    settings,
)
from gemini_service import create_gemini_service
from gradcam import generate_gradcam_base64
from hospital_data import get_all_cities, get_all_hospitals
from image_processing import preprocess_for_inference, validate_image_bytes
from model_loader import model_loader

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SkinGuard AI backend starting up...")
    try:
        model_loader.load(settings.MODEL_PATH)
        logger.info("Model loaded: %s", settings.MODEL_PATH)
    except FileNotFoundError as exc:
        logger.warning("Model not found on startup: %s", exc)
    except Exception as exc:
        logger.error("Unexpected error loading model: %s", exc)

    app.state.gemini = create_gemini_service(
        api_key=settings.GEMINI_API_KEY,
        model_name=settings.GEMINI_MODEL,
    )
    logger.info("Gemini service ready. Available: %s", app.state.gemini.is_available)
    yield
    logger.info("SkinGuard AI backend shutting down.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class PredictionClass(BaseModel):
    label: str
    probability: float


class PredictionResponse(BaseModel):
    success: bool
    diagnosis: str
    confidence: float
    risk_level: str
    risk_label: str
    description: str
    recommendation: str
    all_probabilities: list[PredictionClass]


class GradCAMResponse(BaseModel):
    success: bool
    diagnosis: str
    confidence: float
    gradcam_image: str
    conv_layer_used: str


class ChatRequest(BaseModel):
    message: str
    diagnosis_context: Optional[str] = None


class ChatResponse(BaseModel):
    success: bool
    response: str
    source: str


class HospitalEntry(BaseModel):
    city: str
    name: str
    type: str
    address: str
    maps: str


class HospitalResponse(BaseModel):
    success: bool
    total: int
    hospitals: list[HospitalEntry]


class CitiesResponse(BaseModel):
    success: bool
    total: int
    cities: list[str]


# ---------------------------------------------------------------------------
# Helper: build prediction result from raw probabilities
# ---------------------------------------------------------------------------
def _build_prediction_result(probabilities: np.ndarray) -> dict:
    predicted_index = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_index])
    diagnosis = CLASS_LABELS[predicted_index]
    risk_level = CLASS_RISK_LEVEL[diagnosis]

    all_probs = [
        PredictionClass(label=CLASS_LABELS[i], probability=float(probabilities[i]))
        for i in range(len(CLASS_LABELS))
    ]

    return {
        "predicted_index": predicted_index,
        "confidence": confidence,
        "diagnosis": diagnosis,
        "risk_level": risk_level,
        "risk_label": RISK_DISPLAY[risk_level],
        "description": CLASS_DESCRIPTIONS[diagnosis],
        "recommendation": RISK_RECOMMENDATIONS[risk_level],
        "all_probabilities": all_probs,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/", summary="Root endpoint")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", summary="Health check")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_loader.is_loaded,
        "gemini_available": app.state.gemini.is_available,
        "version": settings.APP_VERSION,
    }


@app.post("/predict", response_model=PredictionResponse, summary="Predict skin disease from image")
async def predict(
    file: UploadFile = File(..., description="Skin lesion image (JPEG/PNG/WEBP, max 10 MB)"),
):
    if not model_loader.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Please check server configuration.",
        )

    image_bytes = await file.read()

    try:
        validate_image_bytes(image_bytes, file.content_type or "")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    try:
        preprocessed, _ = preprocess_for_inference(image_bytes)
        raw_probs = model_loader.predict(preprocessed)[0]
        result = _build_prediction_result(raw_probs)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except Exception as exc:
        logger.exception("Prediction failed.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {exc}",
        )

    return PredictionResponse(
        success=True,
        diagnosis=result["diagnosis"],
        confidence=result["confidence"],
        risk_level=result["risk_level"],
        risk_label=result["risk_label"],
        description=result["description"],
        recommendation=result["recommendation"],
        all_probabilities=result["all_probabilities"],
    )


@app.post("/gradcam", response_model=GradCAMResponse, summary="Generate GradCAM visualization")
async def gradcam(
    file: UploadFile = File(..., description="Skin lesion image (JPEG/PNG/WEBP, max 10 MB)"),
):
    if not model_loader.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Please check server configuration.",
        )

    image_bytes = await file.read()

    try:
        validate_image_bytes(image_bytes, file.content_type or "")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    try:
        preprocessed, pil_image = preprocess_for_inference(image_bytes)
        keras_model = model_loader.get_model()
        raw_probs = model_loader.predict(preprocessed)[0]
        predicted_index = int(np.argmax(raw_probs))
        confidence = float(raw_probs[predicted_index])
        diagnosis = CLASS_LABELS[predicted_index]

        # Detect conv layer name for response metadata
        from gradcam import _find_last_conv_layer

        conv_layer = _find_last_conv_layer(keras_model) or "auto"

        gradcam_b64 = generate_gradcam_base64(
            model=keras_model,
            preprocessed_image=preprocessed,
            original_pil_image=pil_image,
            class_index=predicted_index,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except Exception as exc:
        logger.exception("GradCAM generation failed.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GradCAM error: {exc}",
        )

    return GradCAMResponse(
        success=True,
        diagnosis=diagnosis,
        confidence=confidence,
        gradcam_image=gradcam_b64,
        conv_layer_used=conv_layer,
    )


@app.post("/chat", response_model=ChatResponse, summary="AI medical chat assistant")
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty.",
        )

    result = app.state.gemini.chat(
        message=request.message,
        diagnosis_context=request.diagnosis_context,
    )

    return ChatResponse(
        success=result["success"],
        response=result["response"],
        source=result["source"],
    )


@app.get("/hospitals", response_model=HospitalResponse, summary="Get hospital list")
async def get_hospitals(
    city: Optional[str] = None,
    type: Optional[str] = None,
):
    hospitals = get_all_hospitals(city=city, hospital_type=type)
    return HospitalResponse(
        success=True,
        total=len(hospitals),
        hospitals=[HospitalEntry(**h) for h in hospitals],
    )


@app.get("/hospitals/cities", response_model=CitiesResponse, summary="Get available cities")
async def get_cities():
    cities = get_all_cities()
    return CitiesResponse(
        success=True,
        total=len(cities),
        cities=cities,
    )
