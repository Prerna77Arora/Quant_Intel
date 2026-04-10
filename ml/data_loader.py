import yfinance as yf
import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def fetch_stock_data(symbol: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch stock data with multi-market fallback and clean formatting.
    """

    try:
        possible_symbols = [
            symbol,
            f"{symbol}.NS",   # NSE (India)
            f"{symbol}.BO"    # BSE (India)
        ]

        for sym in possible_symbols:
            df = yf.download(sym, period=period, interval=interval, progress=False)

            if df is not None and not df.empty:
                df.reset_index(inplace=True)

                # 🔹 Standardize column names
                df.columns = [col.lower() for col in df.columns]

                # 🔹 Keep only required columns
                required_cols = ["date", "open", "high", "low", "close", "volume"]
                df = df[[col for col in required_cols if col in df.columns]]

                # 🔹 Sort data (important for LSTM)
                df = df.sort_values("date")

                logger.info(f"Fetched {len(df)} rows for {sym}")
                return df

            logger.warning(f"No data for {sym}")

        logger.error(f"No data found for {symbol} in any format")
        return pd.DataFrame()

    except Exception as e:
        logger.exception(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()


# ---------------- FEATURE ENGINEERING ---------------- #

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add basic indicators for better ML performance.
    """

    try:
        if df.empty:
            return df

        # 🔹 Moving averages
        df["ma10"] = df["close"].rolling(window=10).mean()
        df["ma50"] = df["close"].rolling(window=50).mean()

        # 🔹 Returns
        df["returns"] = df["close"].pct_change()

        # 🔹 Volatility
        df["volatility"] = df["returns"].rolling(window=10).std()

        # 🔹 Drop NaNs after feature creation
        df.dropna(inplace=True)

        return df

    except Exception as e:
        logger.exception(f"Feature engineering failed: {e}")
        return df