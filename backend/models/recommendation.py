from sqlalchemy import Column, Integer, Float, String, ForeignKey, Text
from backend.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False, index=True)

    action = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    predicted_trend = Column(String, nullable=False)

    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    allocation = Column(Float, nullable=False)

    reason = Column(Text, nullable=True)  # 🔥 changed to Text
    risk_explanation = Column(Text, nullable=True)
    strategy = Column(String, nullable=True)