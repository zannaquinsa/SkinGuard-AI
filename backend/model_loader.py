import os
import logging
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


class ModelLoader:
    """Singleton loader for the SkinGuard Keras model."""

    _instance: Optional["ModelLoader"] = None
    _model = None
    _model_loaded: bool = False

    def __new__(cls) -> "ModelLoader":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self, model_path: str) -> None:
        """Load the Keras model from the given path."""
        if self._model_loaded:
            logger.info("Model already loaded, skipping.")
            return

        if not os.path.exists(model_path):
            logger.error("Model file not found: %s", model_path)
            raise FileNotFoundError(
                f"Model file not found at '{model_path}'. "
                "Please place your skinguard_model.keras file in the models/ directory."
            )

        try:
            import tensorflow as tf


            class BatchNormalizationCompat(tf.keras.layers.BatchNormalization):
                def __init__(
                    self,
                    *args,
                    renorm=False,
                    renorm_clipping=None,
                    renorm_momentum=0.99,
                    **kwargs
                ):
                    super().__init__(*args, **kwargs)


            custom_objects = {
                "BatchNormalization": BatchNormalizationCompat,
            }

            self._model = tf.keras.models.load_model(
                model_path,
                compile=False,
                custom_objects=custom_objects,
                safe_mode=False,
            )         
            self._model_loaded = True
            logger.info("Model loaded successfully.")
        except Exception as exc:
            logger.exception("Failed to load model: %s", exc)
            raise RuntimeError(f"Model loading failed: {exc}") from exc

    def predict(self, preprocessed_image: np.ndarray) -> np.ndarray:
        """
        Run inference with Test-Time Augmentation (TTA).

        TTA:
        1. Prediksi gambar asli
        2. Prediksi gambar flip horizontal
        3. Rata-rata probabilitas keduanya
        """
        if not self._model_loaded or self._model is None:
            raise RuntimeError("Model is not loaded. Call load() first.")

        pred_original = self._model.predict(preprocessed_image, verbose=0)

        flipped_image = np.flip(preprocessed_image, axis=2).copy()
        pred_flipped = self._model.predict(flipped_image, verbose=0)

        predictions = (pred_original + pred_flipped) / 2.0
        return predictions

    def get_model(self):
        """Return the underlying Keras model."""
        if not self._model_loaded or self._model is None:
            raise RuntimeError("Model is not loaded. Call load() first.")
        return self._model

    @property
    def is_loaded(self) -> bool:
        return self._model_loaded


model_loader = ModelLoader()
