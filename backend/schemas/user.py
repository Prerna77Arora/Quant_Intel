from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    risk_tolerance: str   # ✅ fixed
    investment_horizon: Optional[str] = None
    budget: Optional[float] = None

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    risk_tolerance: Optional[str] = None   # ✅ fixed
    investment_horizon: Optional[str] = None
    budget: Optional[float] = Field(None, gt=0)