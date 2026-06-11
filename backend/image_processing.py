import io
import logging
from typing import Tuple

import numpy as np
from PIL import Image, ImageOps

from config import settings

logger = logging.getLogger(__name__)

TARGET_SIZE: Tuple[int, int] = (settings.IMAGE_SIZE, settings.IMAGE_SIZE)


def validate_image_bytes(image_bytes: bytes, content_type: str) -> None:
    """Validate image format and size before processing."""
    if content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise ValueError(
            f"Unsupported image format '{content_type}'. "
            f"Allowed formats: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )

    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise ValueError(
            f"Image size {size_mb:.1f} MB exceeds maximum allowed size "
            f"of {settings.MAX_UPLOAD_SIZE_MB} MB."
        )


def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """Load a PIL Image from raw bytes."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)
        if image.mode != "RGB":
            image = image.convert("RGB")
        return image
    except Exception as exc:
        logger.exception("Failed to load image from bytes.")
        raise ValueError(f"Cannot read image data: {exc}") from exc


def resize_image(image: Image.Image, target_size: Tuple[int, int] = TARGET_SIZE) -> Image.Image:
    """Resize image to target size using high-quality Lanczos resampling."""
    return image.resize(target_size, Image.Resampling.LANCZOS)


def normalize_image(image: Image.Image) -> np.ndarray:
    """Convert PIL Image to float32 numpy array in range [0, 255]."""
    array = np.array(image, dtype=np.float32)
    return array


def preprocess_for_inference(image_bytes: bytes) -> Tuple[np.ndarray, Image.Image]:
    """
    Full preprocessing pipeline for model inference.

    Returns:
        preprocessed_batch: np.ndarray with shape (1, 224, 224, 3)
        original_image: PIL Image (RGB, resized) for GradCAM use
    """
    pil_image = load_image_from_bytes(image_bytes)
    resized_image = resize_image(pil_image)
    normalized_array = normalize_image(resized_image)
    batch = np.expand_dims(normalized_array, axis=0)
    return batch, resized_image


def image_to_base64(image: Image.Image, fmt: str = "PNG") -> str:
    """Convert PIL Image to base64-encoded string."""
    import base64

    buffer = io.BytesIO()
    image.save(buffer, format=fmt)
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    return encoded


def overlay_gradcam_on_image(
    original_image: Image.Image,
    heatmap: np.ndarray,
    alpha: float = 0.5,
) -> Image.Image:
    """
    Overlay a GradCAM heatmap (H x W, values in [0,1]) onto the original image.

    Args:
        original_image: PIL Image (RGB)
        heatmap: numpy array of shape (H, W) with values in [0, 1]
        alpha: blending weight for the heatmap overlay

    Returns:
        PIL Image with GradCAM overlay applied
    """
    import cv2

    # Convert heatmap to colormap
    heatmap_uint8 = np.uint8(255 * heatmap)
    colormap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    colormap_rgb = cv2.cvtColor(colormap, cv2.COLOR_BGR2RGB)

    # Resize colormap to match original image dimensions
    original_array = np.array(original_image.resize(TARGET_SIZE))
    colormap_resized = cv2.resize(colormap_rgb, TARGET_SIZE)

    # Blend original image with heatmap
    blended = cv2.addWeighted(original_array, 1 - alpha, colormap_resized, alpha, 0)
    return Image.fromarray(blended)
