import torch
import torch.nn as nn
import torch.optim as optim
import logging

from ml.data_loader import fetch_stock_data
from ml.features import add_features
from ml.preprocessing import prepare_sequences
from ml.model import LSTMModel
from ml.utils import save_model
from ml.config import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def train(symbol="AAPL"):
    try:
        # ---------------- FETCH DATA ---------------- #
        df = fetch_stock_data(symbol)

        if df is None or df.empty:
            logger.error("No data fetched. Exiting training.")
            return

        logger.info(f"Fetched {len(df)} rows")

        # ---------------- FEATURES ---------------- #
        df = add_features(df)
        df.dropna(inplace=True)

        if df.empty:
            logger.error("No data after feature engineering.")
            return

        # 🔹 Updated lowercase columns
        required_cols = ["close", "ma10", "ma50", "volatility", "rsi"]

        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            logger.error(f"Missing columns: {missing}")
            return

        features = df[required_cols].values

        # ---------------- SEQUENCES ---------------- #
        X, y = prepare_sequences(features)

        if len(X) == 0:
            logger.error("No sequences generated.")
            return

        logger.info(f"Training samples: {len(X)}")

        # ---------------- DEVICE ---------------- #
        device = torch.device(config.DEVICE)

        X = torch.tensor(X, dtype=torch.float32).to(device)
        y = torch.tensor(y, dtype=torch.float32).to(device)

        # ---------------- MODEL ---------------- #
        model = LSTMModel(input_size=X.shape[2]).to(device)

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=config.LR)

        # ---------------- TRAIN LOOP ---------------- #
        for epoch in range(config.EPOCHS):
            model.train()

            outputs = model(X).squeeze()
            loss = criterion(outputs, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            logger.info(
                f"Epoch {epoch+1}/{config.EPOCHS} | Loss: {loss.item():.6f}"
            )

        # ---------------- SAVE MODEL ---------------- #
        save_model(model)

        logger.info("Training completed successfully")

    except Exception as e:
        logger.exception(f"Training failed: {e}")


# ---------------- ENTRY POINT ---------------- #
if __name__ == "__main__":
    print("🚀 Starting training...")
    train("AAPL")