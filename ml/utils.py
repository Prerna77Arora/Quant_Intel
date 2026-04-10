import torch
import os
import logging
from ml.config import config

logger = logging.getLogger(__name__)


# ---------------- SAVE MODEL ---------------- #
def save_model(model):
    """
    Save trained model weights.
    """
    try:
        os.makedirs(config.MODEL_DIR, exist_ok=True)

        torch.save(model.state_dict(), config.MODEL_PATH)

        logger.info(f"Model saved at {config.MODEL_PATH}")

    except Exception as e:
        logger.exception("Model saving failed")
        raise e


# ---------------- LOAD MODEL ---------------- #
def load_model(model_class, input_size):
    """
    Load trained model safely with device handling.
    """

    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {config.MODEL_PATH}. Train model first."
        )

    try:
        device = torch.device(config.DEVICE)

        model = model_class(input_size)
        model.load_state_dict(
            torch.load(config.MODEL_PATH, map_location=device)
        )

        model.to(device)
        model.eval()

        logger.info("Model loaded successfully")

        return model

    except Exception as e:
        logger.exception("Model loading failed")
        raise e