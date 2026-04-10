from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from datetime import datetime
from backend.core.database import Base


class ChatbotSession(Base):
    __tablename__ = "chatbot_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    current_step = Column(Integer, default=0)
    completed = Column(Boolean, default=False)

    risk_response = Column(String, nullable=True)
    budget_response = Column(Float, nullable=True)
    horizon_response = Column(String, nullable=True)
    experience_response = Column(String, nullable=True)
    sectors_response = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("chatbot_sessions.id"), nullable=False, index=True)

    role = Column(String, default="user")  # 🔥 FIX
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)