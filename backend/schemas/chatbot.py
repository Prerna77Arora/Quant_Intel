from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatbotSessionCreate(BaseModel):
    pass  # OK if nothing required at creation

class ChatbotSessionResponse(BaseModel):
    id: int
    user_id: int
    current_step: int
    completed: bool
    risk_response: Optional[str] = None
    budget_response: Optional[float] = None
    horizon_response: Optional[str] = None
    experience_response: Optional[str] = None
    sectors_response: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatbotStepRequest(BaseModel):
    step: int
    response: str  # generic string (convert later if needed)

class ChatbotStepResponse(BaseModel):
    step: int
    completed: bool
    next_question: str
    message: str

    class Config:
        from_attributes = True

class ChatbotSessionState(BaseModel):
    session_id: int
    current_step: int
    completed: bool
    question: str

    class Config:
        from_attributes = True