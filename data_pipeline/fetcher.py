import yfinance as yf
import time
from data_pipeline.logger import logger
from data_pipeline.config import config


def fetch_stock(symbol):
    for attempt in range(config.RETRY_COUNT):
        try:
            df = yf.download(
                symbol,
                period="1mo",                 # ⬅️ more data for ML
                interval=config.DATA_INTERVAL
            )

            # ---------------------- VALIDATION ---------------------- #
            if df.empty:
                raise ValueError(f"No data returned for {symbol}")

            df.reset_index(inplace=True)

            # ---------------------- CLEANING ---------------------- #
            df.rename(columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            }, inplace=True)

            df = df[["date", "open", "high", "low", "close", "volume"]]

            # ---------------------- FEATURE HOOK (for ML later) ---------------------- #
            df["returns"] = df["close"].pct_change()
            df["ma_5"] = df["close"].rolling(window=5).mean()

            df.dropna(inplace=True)

            logger.info(f"Fetched & processed data for {symbol}")

            return df

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed for {symbol}: {e}")
            time.sleep(config.RETRY_DELAY)

    raise Exception(f"Failed to fetch data for {symbol} after retries")