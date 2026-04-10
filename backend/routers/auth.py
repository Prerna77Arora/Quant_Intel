from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.schemas.auth import LoginRequest, TokenResponse
from backend.schemas.user import UserCreate
from backend.services.auth_service import (
    register_user,
    authenticate_user,
    generate_tokens
)
from backend.utils.dependencies import get_db, get_current_user


# ✅ FIX: Removed prefix from here
router = APIRouter(tags=["Auth"])


# ---------------------- REGISTER ---------------------- #
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, data.email, data.password)

    return {
        "success": True,
        "data": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        },
        "message": "Registration successful"
    }


# ---------------------- LOGIN ---------------------- #
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    tokens = generate_tokens(user)

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "expires_in": 30 * 60  # 30 minutes in seconds
    }


# ---------------------- LOGOUT ---------------------- #
@router.post("/logout")
def logout(user=Depends(get_current_user)):
    return {
        "success": True,
        "message": "Logout successful"
    }


# ---------------------- GET CURRENT USER ---------------------- #
@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "risk_level": user.risk_level,
            "budget": user.budget,
            "investment_horizon": user.investment_horizon
        }
    }