import pandas as pd
from data_pipeline.logger import logger


def clean_data(df: pd.DataFrame, symbol: str):
    try:
        # ---------------------- FIX MULTI-INDEX ---------------------- #
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

        # ---------------------- STANDARDIZE COLUMNS ---------------------- #
        df = df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

        # ---------------------- VALIDATION ---------------------- #
        required_cols = ["date", "open", "high", "low", "close", "volume"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        # ---------------------- RESET INDEX ---------------------- #
        df = df.reset_index(drop=True)

        # ---------------------- ADD SYMBOL ---------------------- #
        df["symbol"] = symbol

        # ---------------------- TYPE FIXES ---------------------- #
        df["date"] = pd.to_datetime(df["date"]).dt.date

        numeric_cols = ["open", "high", "low", "close", "volume"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

        # ---------------------- FEATURE ENGINEERING ---------------------- #
        df["returns"] = df["close"].pct_change()
        df["ma_5"] = df["close"].rolling(window=5).mean()
        df["volatility"] = df["close"].rolling(window=5).std()

        # ---------------------- FINAL CLEAN ---------------------- #
        df = df[[
            "symbol", "date", "open", "high", "low", "close", "volume",
            "returns", "ma_5", "volatility"
        ]]

        df.dropna(inplace=True)

        logger.info(f"Cleaned & enriched data for {symbol}")

        return df

    except Exception as e:
        logger.error(f"Preprocessing error for {symbol}: {e}")
        raise