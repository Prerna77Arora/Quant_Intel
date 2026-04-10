from pydantic import BaseModel, Field

class RecommendationResponse(BaseModel):
    stock_id: int
    action: str  # BUY / SELL / HOLD
    confidence: float = Field(..., ge=0, le=1)
    predicted_trend: str
    stop_loss: float
    take_profit: float
    allocation: float = Field(..., ge=0, le=1)
    reason: str
    risk_explanation: str
    strategy: str

    class Config:
        from_attributes = True