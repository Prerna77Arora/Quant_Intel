import os


class Config:
    # ---------------- PATHS ---------------- #
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DATA_PATH = os.getenv("DATA_PATH", os.path.join(BASE_DIR, "data"))
    MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(BASE_DIR, "models"))
    LOG_PATH = os.getenv("LOG_PATH", os.path.join(BASE_DIR, "logs"))

    MODEL_NAME = "lstm_model.pt"
    MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

    # ---------------- TRAINING PARAMS ---------------- #
    SEQ_LENGTH = int(os.getenv("SEQ_LENGTH", 60))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
    EPOCHS = int(os.getenv("EPOCHS", 10))
    LR = float(os.getenv("LR", 0.001))

    # ---------------- MODEL PARAMS ---------------- #
    HIDDEN_SIZE = int(os.getenv("HIDDEN_SIZE", 64))
    NUM_LAYERS = int(os.getenv("NUM_LAYERS", 2))
    INPUT_SIZE = 1        # stock price (can expand later)
    OUTPUT_SIZE = 1       # next price prediction

    # ---------------- FEATURES ---------------- #
    USE_SCALER = True     # normalize data
    SAVE_CHECKPOINTS = True

    # ---------------- INFERENCE ---------------- #
    DEVICE = os.getenv("DEVICE", "cpu")  # can be "cuda"

    # ---------------- API INTEGRATION ---------------- #
    DEFAULT_STOCK = "AAPL"   # fallback for testing
    PREDICTION_DAYS = 7      # future days to predict


# Singleton config instance
config = Config()