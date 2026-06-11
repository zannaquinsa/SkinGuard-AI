import logging
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


def _find_last_conv_layer(model) -> Optional[str]:
    """Scan the model in reverse to find the last convolutional layer name."""
    for layer in reversed(model.layers):
        if hasattr(layer, "filters") or "conv" in layer.name.lower():
            return layer.name
    return None


def compute_gradcam(
    model,
    preprocessed_image: np.ndarray,
    class_index: int,
    conv_layer_name: Optional[str] = None,
) -> np.ndarray:
    """
    Compute a GradCAM heatmap for the given image and predicted class.

    Args:
        model: Loaded Keras model
        preprocessed_image: np.ndarray of shape (1, H, W, 3), normalized
        class_index: index of the target class
        conv_layer_name: name of the convolutional layer to use. Auto-detected if None.

    Returns:
        heatmap: np.ndarray of shape (H, W) with values in [0, 1]
    """
    import tensorflow as tf

    if conv_layer_name is None:
        conv_layer_name = _find_last_conv_layer(model)

    if conv_layer_name is None:
        logger.warning("No convolutional layer found. Returning blank heatmap.")
        h, w = preprocessed_image.shape[1], preprocessed_image.shape[2]
        return np.zeros((h, w), dtype=np.float32)

    try:
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[
                model.get_layer(conv_layer_name).output,
                model.output,
            ],
        )

        with tf.GradientTape() as tape:
            inputs = tf.cast(preprocessed_image, tf.float32)
            conv_outputs, predictions = grad_model(inputs)
            target_class_score = predictions[:, class_index]

        grads = tape.gradient(target_class_score, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        return heatmap.numpy()

    except Exception as exc:
        logger.exception("GradCAM computation failed: %s", exc)
        h, w = preprocessed_image.shape[1], preprocessed_image.shape[2]
        return np.zeros((h, w), dtype=np.float32)


def generate_gradcam_base64(
    model,
    preprocessed_image: np.ndarray,
    original_pil_image,
    class_index: int,
    conv_layer_name: Optional[str] = None,
) -> str:
    """
    Full pipeline: compute GradCAM heatmap, overlay on original image,
    and return the result as a base64-encoded PNG string.

    Args:
        model: Loaded Keras model
        preprocessed_image: np.ndarray of shape (1, 224, 224, 3)
        original_pil_image: PIL Image (RGB)
        class_index: predicted class index
        conv_layer_name: optional override for the conv layer name

    Returns:
        base64-encoded PNG string
    """
    from image_processing import image_to_base64, overlay_gradcam_on_image

    heatmap = compute_gradcam(model, preprocessed_image, class_index, conv_layer_name)
    overlaid = overlay_gradcam_on_image(original_pil_image, heatmap)
    return image_to_base64(overlaid, fmt="PNG")
