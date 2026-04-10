from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from backend.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # 🔥 FIX: add index
    email = Column(String, unique=True, nullable=False, index=True)

    # 🔥 FIX: clearer naming
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # User Profile (Chatbot)
    risk_tolerance = Column(String, default="medium")  # low, medium, high
    budget = Column(Float, nullable=True)
    investment_horizon = Column(String, nullable=True)
    experience_level = Column(String, default="beginner")
    preferred_sectors = Column(String, nullable=True)

    profile_complete = Column(Boolean, default=False)

    # 🔁 Compatibility mapping
    @property
    def risk_level(self):
        return self.risk_tolerance

    @risk_level.setter
    def risk_level(self, value):
        self.risk_tolerance = value

    def __repr__(self):
        return f"<User(email={self.email}, risk={self.risk_tolerance})>"