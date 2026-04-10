import numpy as np
import joblib
import os
import logging
from sklearn.preprocessing import MinMaxScaler
from ml.config import config

logger = logging.getLogger(__name__)

SCALER_PATH = os.path.join(config.MODEL_DIR, "scaler.pkl")

# 🔹 Global scaler instance
scaler = MinMaxScaler()


# ---------------- TRAINING SCALER ---------------- #
def fit_scaler(data):
    """
    Fit scaler on training data and save it.
    """
    try:
        scaler.fit(data)

        os.makedirs(config.MODEL_DIR, exist_ok=True)
        joblib.dump(scaler, SCALER_PATH)

        logger.info("Scaler fitted and saved")

    except Exception as e:
        logger.exception("Scaler fitting failed")
        raise e


# ---------------- LOAD SCALER ---------------- #
def load_scaler():
    """
    Load pre-trained scaler.
    """
    global scaler

    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError("Scaler not found. Train model first.")

    scaler = joblib.load(SCALER_PATH)
    logger.info("Scaler loaded successfully")

    return scaler


# ---------------- PREPARE SEQUENCES ---------------- #
def prepare_sequences(data):
    """
    Prepare sequences for LSTM training.
    """

    if data is None or len(data) == 0:
        raise ValueError("Data cannot be empty")

    try:
        # 🔹 Fit scaler ONLY during training
        fit_scaler(data)
        scaled = scaler.transform(data)

    except Exception as e:
        raise ValueError(f"Scaling failed: {str(e)}")

    X, y = [], []
    seq_len = config.SEQ_LENGTH

    for i in range(seq_len, len(scaled)):
        X.append(scaled[i - seq_len:i])
        y.append(scaled[i][0])  # predict close price

    if len(X) == 0:
        raise ValueError(
            f"Need at least {seq_len} rows, got {len(scaled)}"
        )

    return np.array(X), np.array(y)