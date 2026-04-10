import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ---------------------- DATABASE ---------------------- #
    # Supabase PostgreSQL connection
    POSTGRES_URL = os.getenv(
        "POSTGRES_URL",
        "postgresql://user:password@localhost/trademind"
    )

    # ---------------------- API KEYS ---------------------- #
    # For stock data (Alpha Vantage / Yahoo / Polygon later)
    STOCK_API_KEY = os.getenv("STOCK_API_KEY", "")

    # ---------------------- STOCK CONFIG ---------------------- #
    # Default symbols (can later come from DB/user preference)
    STOCK_SYMBOLS = os.getenv("STOCK_SYMBOLS", "AAPL,MSFT,GOOGL").split(",")

    # Data interval (useful for pipeline + ML)
    DATA_INTERVAL = os.getenv("DATA_INTERVAL", "1d")  # 1d, 1h, etc.

    # ---------------------- ML CONFIG ---------------------- #
    MODEL_PATH = os.getenv("MODEL_PATH", "models/trademind_model.pth")

    # Prediction settings
    PREDICTION_DAYS = int(os.getenv("PREDICTION_DAYS", 7))

    # ---------------------- PIPELINE CONFIG ---------------------- #
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", 5))

    # Batch processing size (important for scaling)
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))

    # ---------------------- LOGGING ---------------------- #
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


config = Config()