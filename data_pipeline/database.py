from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# ---------------------- DATABASE SETUP ---------------------- #
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ---------------------- STOCK DATA TABLE ---------------------- #
class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(Date, index=True)

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------------- PREDICTIONS TABLE ---------------------- #
class StockPrediction(Base):
    __tablename__ = "stock_predictions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(Date)

    predicted_price = Column(Float)
    confidence = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------------- RECOMMENDATIONS TABLE ---------------------- #
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)

    action = Column(String)
    target_price = Column(Float)
    stop_loss = Column(Float)
    confidence = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)


# ❌ DO NOT create tables here