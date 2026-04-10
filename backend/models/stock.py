from sqlalchemy import Column, Integer, String, Float
from backend.core.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)

    # Stock identity
    symbol = Column(String, unique=True, nullable=False, index=True)

    # Classification
    sector = Column(String, nullable=False)
    industry = Column(String, nullable=False)

    # Financial attributes
    market_cap = Column(Float, nullable=False)
    style = Column(String, nullable=False)  # Growth / Value

    # 🔥 IMPORTANT: normalize risk values
    risk_level = Column(String, nullable=False)  # low / medium / high

    def __repr__(self):
        return f"<Stock(symbol={self.symbol}, risk={self.risk_level})>"