from ml.predict import predict_stock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.user import User
import logging

logger = logging.getLogger(__name__)


def get_prediction(symbol: str):
    """
    Basic ML prediction wrapper
    """
    if not symbol or not isinstance(symbol, str):
        raise HTTPException(status_code=400, detail="Invalid stock symbol")

    try:
        result = predict_stock(symbol)
        logger.info(f"Prediction generated for {symbol}")
        return result

    except ValueError as e:
        logger.error(f"Validation error for {symbol}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Prediction error for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")


# ✅ MAIN INTELLIGENCE LAYER (IMPORTANT)
def get_recommendation(db: Session, user_id: int, symbol: str):
    """
    Personalized recommendation using:
    - ML prediction
    - User profile (risk, budget, horizon)
    """

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.profile_complete:
        raise HTTPException(
            status_code=400,
            detail="Complete chatbot profile first"
        )

    prediction = get_prediction(symbol)

    # 👉 Expected ML output format (you should align this)
    # {
    #   "current_price": 100,
    #   "predicted_price": 115,
    #   "confidence": 0.82
    # }

    current_price = prediction.get("current_price")
    predicted_price = prediction.get("predicted_price")
    confidence = prediction.get("confidence", 0.5)

    if not current_price or not predicted_price:
        raise HTTPException(status_code=500, detail="Invalid prediction output")

    expected_return = (predicted_price - current_price) / current_price

    # ✅ Decision logic (core of TradeMind)
    if user.risk_level == "low":
        threshold = 0.05
    elif user.risk_level == "medium":
        threshold = 0.10
    else:  # high
        threshold = 0.15

    if expected_return > threshold:
        action = "BUY"
    elif expected_return < -threshold:
        action = "SELL"
    else:
        action = "HOLD"

    # ✅ Risk-adjusted stop loss
    stop_loss = current_price * (1 - threshold)
    target = predicted_price

    return {
        "symbol": symbol,
        "action": action,
        "current_price": current_price,
        "predicted_price": predicted_price,
        "expected_return": round(expected_return * 100, 2),
        "confidence": confidence,
        "target": round(target, 2),
        "stop_loss": round(stop_loss, 2),
        "risk_tolerance": user.risk_tolerance,
        "explanation": generate_explanation(action, expected_return, user.risk_level)
    }


def generate_explanation(action, expected_return, risk_level):
    """
    Simple explainability layer (VERY IMPORTANT for judges)
    """

    if action == "BUY":
        return f"Stock shows strong upside (~{round(expected_return*100,2)}%) aligned with your {risk_level} risk profile."
    elif action == "SELL":
        return f"Downside risk detected (~{round(expected_return*100,2)}%). Suitable to exit based on your {risk_level} risk tolerance."
    else:
        return f"Stock movement is uncertain. Holding is safer for your {risk_level} risk profile."