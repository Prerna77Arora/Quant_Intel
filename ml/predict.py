import torch
import numpy as np
import logging

from ml.data_loader import fetch_stock_data
from ml.features import add_features
from ml.preprocessing import scaler  # should be pre-fitted & saved
from ml.model import LSTMModel
from ml.utils import load_model
from ml.config import config

logger = logging.getLogger(__name__)


def predict_stock(symbol: str):
    """
    Predict next stock price using trained LSTM model.
    """

    try:
        # ---------------- FETCH DATA ---------------- #
        df = fetch_stock_data(symbol)

        if df is None or df.empty:
            raise ValueError(f"No valid data fetched for {symbol}")

        logger.info(f"Fetched {len(df)} rows for {symbol}")

        # ---------------- FEATURES ---------------- #
        df = add_features(df)

        if df.empty:
            raise ValueError("No data after feature engineering")

        # 🔹 Updated lowercase columns
        required_cols = ["close", "ma10", "ma50", "volatility", "rsi"]

        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing features: {missing}")

        features = df[required_cols].values

        # ---------------- SCALING ---------------- #
        try:
            # ❗ IMPORTANT: Use transform, NOT fit_transform
            scaled = scaler.transform(features)
        except Exception as e:
            logger.exception("Scaling failed")
            raise ValueError("Scaler not fitted or missing")

        # ---------------- SEQUENCE ---------------- #
        if len(scaled) < config.SEQ_LENGTH:
            raise ValueError(
                f"Need {config.SEQ_LENGTH} rows, got {len(scaled)}"
            )

        seq = scaled[-config.SEQ_LENGTH:]
        seq = torch.tensor(seq, dtype=torch.float32).unsqueeze(0)

        # ---------------- MODEL ---------------- #
        device = torch.device(config.DEVICE)
        seq = seq.to(device)

        model = load_model(LSTMModel, input_size=seq.shape[2])
        model.to(device)
        model.eval()

        # ---------------- PREDICTION ---------------- #
        with torch.no_grad():
            pred_scaled = model(seq).cpu().numpy()

        # ---------------- INVERSE SCALING ---------------- #
        # Reconstruct full feature vector for inverse transform
        dummy = np.zeros((1, features.shape[1]))
        dummy[0, 0] = pred_scaled[0, 0]  # only close price

        pred_actual = scaler.inverse_transform(dummy)[0, 0]

        logger.info(f"Prediction for {symbol}: {pred_actual}")

        return {
            "symbol": symbol,
            "predicted_price": float(pred_actual),
            "status": "success"
        }

    except Exception as e:
        logger.exception(f"Prediction failed for {symbol}")
        return {
            "symbol": symbol,
            "predicted_price": None,
            "status": "error",
            "message": str(e)
        }
def predict_prices(symbol: str):
    """
    Wrapper for pipeline compatibility.
    Calls predict_stock internally.
    """
    return predict_stock(symbol)


# ---------------- ENTRY POINT ---------------- #
if __name__ == "__main__":
    print("🚀 Running prediction...")
    result = predict_stock("AAPL")
    print(result)