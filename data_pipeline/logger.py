import logging
import os
from data_pipeline.config import config


def setup_logger():
    os.makedirs("data_pipeline/logs", exist_ok=True)

    logger = logging.getLogger("TradeMindPipeline")
    logger.setLevel(config.LOG_LEVEL)

    # Prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # ---------------------- FORMAT ---------------------- #
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    # ---------------------- FILE HANDLER ---------------------- #
    file_handler = logging.FileHandler("data_pipeline/logs/pipeline.log")
    file_handler.setFormatter(formatter)

    # ---------------------- CONSOLE HANDLER ---------------------- #
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # ---------------------- ADD HANDLERS ---------------------- #
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()