from sqlalchemy.orm import Session
from data_pipeline.database import SessionLocal, StockData
from data_pipeline.logger import logger


def store_data(df):
    session: Session = SessionLocal()

    try:
        for _, row in df.iterrows():

            # ---------------------- CHECK DUPLICATE ---------------------- #
            existing = session.query(StockData).filter(
                StockData.symbol == row["symbol"],
                StockData.date == row["date"]
            ).first()

            if existing:
                # Optional: update instead of skip
                existing.open = row["open"]
                existing.high = row["high"]
                existing.low = row["low"]
                existing.close = row["close"]
                existing.volume = row["volume"]
            else:
                record = StockData(
                    symbol=row["symbol"],
                    date=row["date"],
                    open=row["open"],
                    high=row["high"],
                    low=row["low"],
                    close=row["close"],
                    volume=row["volume"]
                )
                session.add(record)

        session.commit()
        logger.info("Data stored successfully (no duplicates)")

    except Exception as e:
        session.rollback()
        logger.error(f"DB error: {e}")
        raise

    finally:
        session.close()