import logging
from data_pipeline.fetcher import fetch_stock
from data_pipeline.preprocessing import clean_data
from data_pipeline.storage import store_data
from data_pipeline.config import config

# ✅ ML prediction
from ml.predict import predict_prices

# ✅ Backend recommendation service
from backend.services.recommendation_service import generate_recommendation


logger = logging.getLogger(__name__)


def run():
    """Run pipeline for all configured stock symbols."""
    try:
        results = []

        for symbol in config.STOCK_SYMBOLS:
            try:
                logger.info(f"Fetching data for {symbol}...")

                # ---------------------- DATA PIPELINE ---------------------- #
                df = fetch_stock(symbol)
                df = clean_data(df, symbol)
                store_data(df)

                # ---------------------- ML PREDICTION ---------------------- #
                predictions = predict_prices(symbol)   # ✅ FIXED

                # ---------------------- RECOMMENDATION ---------------------- #
                recommendation = generate_recommendation(df, predictions)

                results.append({
                    "symbol": symbol,
                    "status": "success",
                    "prediction": predictions.get("predicted_price"),  # ✅ FIXED
                    "recommendation": recommendation
                })

                logger.info(f"Successfully processed {symbol}")

            except Exception as e:
                logger.error(f"Error processing {symbol}: {e}")
                results.append({
                    "symbol": symbol,
                    "status": "error",
                    "error": str(e)
                })

        logger.info("Pipeline completed successfully")

        return {
            "status": "success",
            "message": "Data + predictions + recommendations updated",
            "results": results
        }

    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise


def run_single_stock(symbol: str):
    """
    Run pipeline for a single stock symbol.
    Used when stock is not found in DB.
    """
    try:
        logger.info(f"Running pipeline for {symbol}...")

        # ---------------------- DATA PIPELINE ---------------------- #
        df = fetch_stock(symbol)
        df = clean_data(df, symbol)
        store_data(df)

        # ---------------------- ML ---------------------- #
        predictions = predict_prices(symbol)   # ✅ FIXED

        # ---------------------- RECOMMENDATION ---------------------- #
        recommendation = generate_recommendation(df, predictions)

        logger.info(f"Successfully processed {symbol}")

        return {
            "status": "success",
            "symbol": symbol,
            "prediction": predictions.get("predicted_price"),  # ✅ FIXED
            "recommendation": recommendation
        }

    except Exception as e:
        logger.error(f"Single-stock pipeline error for {symbol}: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()