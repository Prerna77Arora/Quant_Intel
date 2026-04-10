from pydantic import BaseModel, Field

class StockCreate(BaseModel):
    symbol: str
    sector: str
    industry: str
    market_cap: float = Field(..., gt=0)
    style: str
    risk_tolerance: str   # ✅ fixed

class StockResponse(BaseModel):
    id: int
    symbol: str
    sector: str
    industry: str
    market_cap: float
    style: str
    risk_tolerance: str   # ✅ fixed

    class Config:
        from_attributes = True