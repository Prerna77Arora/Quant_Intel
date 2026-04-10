import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add technical indicators for ML model.
    Works with standardized lowercase columns from data_loader.
    """

    try:
        if df.empty:
            return df

        # 🔹 Ensure required column exists
        if "close" not in df.columns:
            logger.error("Column 'close' not found in dataframe")
            return df

        # ---------------- MOVING AVERAGES ---------------- #
        df["ma10"] = df["close"].rolling(window=10).mean()
        df["ma50"] = df["close"].rolling(window=50).mean()

        # ---------------- VOLATILITY ---------------- #
        df["volatility"] = df["close"].rolling(window=10).std()

        # ---------------- RSI ---------------- #
        delta = df["close"].diff()

        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        gain = pd.Series(gain).rolling(window=14).mean()
        loss = pd.Series(loss).rolling(window=14).mean()

        # 🔹 Avoid division by zero
        loss = loss.replace(0, 1e-10)

        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # ---------------- RETURNS ---------------- #
        df["returns"] = df["close"].pct_change()

        # ---------------- CLEANUP ---------------- #
        df.dropna(inplace=True)

        logger.info("Feature engineering completed")

        return df

    except Exception as e:
        logger.exception(f"Feature engineering failed: {e}")
        return df