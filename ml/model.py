import torch
import torch.nn as nn
from ml.config import config


class LSTMModel(nn.Module):
    def __init__(self, input_size=None):
        super(LSTMModel, self).__init__()

        # 🔹 Allow dynamic input size (multi-feature support later)
        self.input_size = input_size if input_size else config.INPUT_SIZE

        self.lstm = nn.LSTM(
            input_size=self.input_size,
            hidden_size=config.HIDDEN_SIZE,
            num_layers=config.NUM_LAYERS,
            batch_first=True,
            dropout=0.2 if config.NUM_LAYERS > 1 else 0
        )

        # 🔹 Fully connected output layer
        self.fc = nn.Linear(config.HIDDEN_SIZE, config.OUTPUT_SIZE)

    def forward(self, x):
        """
        x shape: (batch_size, seq_length, input_size)
        """

        # 🔹 LSTM forward pass
        out, _ = self.lstm(x)

        # 🔹 Take last timestep output
        out = out[:, -1, :]

        # 🔹 Final prediction
        out = self.fc(out)

        return out