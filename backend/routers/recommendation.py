from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.services.recommendation_service import generate_recommendations
from backend.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


class RecommendationRequest(BaseModel):
    risk_level: Optional[str] = None


def map_risk_level(risk):
    if not risk:
        return None

    mapping = {
        "conservative": "low",
        "balanced": "medium",
        "aggressive": "high"
    }
    return mapping.get(risk.lower(), "medium")


@router.post("/", status_code=status.HTTP_200_OK)
def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Generate personalized recommendations."""
    try:
        # ✅ Priority: request → user profile → default
        risk_level = (
            map_risk_level(request.risk_level)
            or getattr(user, "risk_tolerance", None)
            or "medium"
        )

        # 🚨 Ensure profile exists (MAIN BUG FIX)
        if not getattr(user, "profile_complete", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complete your profile first using chatbot"
            )

        recommendations = generate_recommendations(
            db=db,
            user_id=user.id,
            user=user,
            risk_level=risk_level
        )

        if not recommendations:
            return {
                "success": False,
                "message": "No recommendations available",
                "data": []
            }

        return {
            "success": True,
            "data": recommendations,
            "message": "Recommendations generated successfully"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )