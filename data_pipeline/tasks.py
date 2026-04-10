from data_pipeline.fetcher import fetch_stock
from data_pipeline.preprocessing import clean_data
from data_pipeline.storage import store_data
from data_pipeline.logger import logger

def run_pipeline(symbol):
    """
    Run pipeline for a single stock symbol.
    """
    try:
        df = fetch_stock(symbol)
        df = clean_data(df, symbol)
        store_data(df)

        logger.info(f"Pipeline completed for {symbol}")

    except Exception as e:
        logger.error(f"Pipeline failed for {symbol}: {e}")
        raise