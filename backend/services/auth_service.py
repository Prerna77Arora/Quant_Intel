from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.user import User
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

def register_user(db: Session, email: str, password: str):
    # ✅ Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # ✅ Create user with default profile values
    user = User(
        email=email,
        hashed_password=hash_password(password),
        role="user",
        risk_tolerance="medium",  # default for TradeMind
        investment_horizon=None,
        budget=None
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return user


def generate_tokens(user: User):
    # ✅ Pass user.id directly (int), not a dict
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }