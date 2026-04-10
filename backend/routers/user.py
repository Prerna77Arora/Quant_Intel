from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.utils.dependencies import get_current_user, get_db, require_role
from backend.schemas.user import UserProfileUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK)
def get_me(user=Depends(get_current_user)):
    """Get current user profile."""
    return {
        "success": True,
        "data": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            # ✅ FIX: consistent field name
            "risk_tolerance": user.risk_tolerance,
            "investment_horizon": user.investment_horizon,
            "budget": user.budget,
            "profile_complete": user.profile_complete
        }
    }


@router.put("/profile", status_code=status.HTTP_200_OK)
def update_profile(
    profile: UserProfileUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user investment profile."""
    try:
        # ✅ FIX: use SAME field everywhere (risk_tolerance)
        if profile.risk_level is not None:
            if profile.risk_level not in ["low", "medium", "high"]:
                raise HTTPException(
                    status_code=400,
                    detail="risk_level must be 'low', 'medium', or 'high'"
                )
            user.risk_tolerance = profile.risk_level

        if profile.investment_horizon is not None:
            if profile.investment_horizon not in ["short-term", "medium-term", "long-term"]:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid investment horizon"
                )
            user.investment_horizon = profile.investment_horizon

        if profile.budget is not None:
            if profile.budget < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Budget must be positive"
                )
            user.budget = profile.budget

        # 🔥 IMPORTANT: mark profile complete
        if user.risk_tolerance and user.investment_horizon and user.budget:
            user.profile_complete = True

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "success": True,
            "data": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "risk_tolerance": user.risk_tolerance,
                "investment_horizon": user.investment_horizon,
                "budget": user.budget,
                "profile_complete": user.profile_complete
            },
            "message": "Profile updated successfully"
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update profile"
        )


@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": "Admin access granted"}