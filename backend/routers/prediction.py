from fastapi import APIRouter, HTTPException, status
from backend.services.prediction_service import get_prediction

router = APIRouter(prefix="/prediction", tags=["Prediction"])


@router.get("/{symbol}", status_code=status.HTTP_200_OK)
def predict(symbol: str):
    """Get stock prediction for a given symbol."""
    try:
        prediction = get_prediction(symbol)

        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prediction not found"
            )

        return {
            "success": True,
            "data": prediction,
            "message": "Prediction fetched successfully"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed"
        )