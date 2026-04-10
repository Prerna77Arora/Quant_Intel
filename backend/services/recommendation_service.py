from backend.services.prediction_service import get_prediction
from backend.models.recommendation import Recommendation
from backend.models.stock import Stock
import logging

logger = logging.getLogger(__name__)

def get_user_risk_preference(user):
    if hasattr(user, 'risk_tolerance') and user.risk_tolerance:
        return user.risk_tolerance
    return "medium"

def calculate_allocation(base_allocation: float, user_risk: str, stock_risk: str) -> float:
    if user_risk == "low":
        allocation = 0.08
        if stock_risk == "high":
            allocation *= 0.5
    elif user_risk == "high":
        allocation = 0.12
        if stock_risk == "high":
            allocation *= 1.2
    else:
        allocation = 0.10
        if stock_risk == "high":
            allocation *= 0.95
    
    return allocation

def get_sector_allocation_limit(user_risk: str) -> int:
    if user_risk == "low":
        return 2
    elif user_risk == "high":
        return 4
    else:
        return 3

def get_recommendation_confidence(user_risk: str, stock_risk: str, prediction_strength: float) -> float:
    base_confidence = 0.75
    
    if user_risk == stock_risk:
        base_confidence += 0.10
    
    base_confidence += (abs(prediction_strength) * 0.1)
    
    return min(base_confidence, 0.99)

def generate_recommendations(db, user_id, user, risk_level=None):

    if not risk_level:
        risk_level = get_user_risk_preference(user)

    # ✅ FIXED: use risk_tolerance
    stocks = db.query(Stock).filter(Stock.risk_tolerance == risk_level).all()
    
    if not stocks:
        logger.warning(f"No stocks found for risk level: {risk_level}")
        return []
    
    recommendations = []
    sector_counts = {}
    sector_limit = get_sector_allocation_limit(risk_level)
    
    for stock in stocks:
        sector = stock.sector
        if sector not in sector_counts:
            sector_counts[sector] = 0
        
        if sector_counts[sector] >= sector_limit:
            logger.debug(f"Skipping {stock.symbol} - sector {sector} limit reached")
            continue
        
        sector_counts[sector] += 1
        
        try:
            prediction = get_prediction(stock.symbol)

            current_price = prediction.get("current_price", 1)
            predicted_price = prediction.get("predicted_price", 0)
            prediction_strength = prediction.get("strength", 0)

            # ✅ FIXED: proper logic
            expected_return = (predicted_price - current_price) / current_price
            
            if risk_level == "low":
                action = "Buy" if expected_return > 0.05 else "Hold"
                confidence = get_recommendation_confidence(risk_level, stock.risk_tolerance, prediction_strength)
                allocation = calculate_allocation(0.08, risk_level, stock.risk_tolerance)
                strategy = "Capital preservation with selective growth"
                risk_exp = "Conservative strategy - focus on stable stocks only. Avoid high volatility."
                
            elif risk_level == "high":
                action = "Buy" if expected_return > -0.02 else "Hold"
                confidence = get_recommendation_confidence(risk_level, stock.risk_tolerance, prediction_strength)
                allocation = calculate_allocation(0.12, risk_level, stock.risk_tolerance)
                strategy = "Growth-focused with calculated risk"
                risk_exp = "Aggressive strategy - includes high-risk/high-reward opportunities. Prepared for volatility."
                
            else:
                action = "Buy" if expected_return > 0 else "Hold"
                confidence = get_recommendation_confidence(risk_level, stock.risk_tolerance, prediction_strength)
                allocation = calculate_allocation(0.10, risk_level, stock.risk_tolerance)
                strategy = "Balanced growth with diversification"
                risk_exp = "Balanced strategy - mix of growth and stability. Moderate volatility tolerance."
            
            recommendation = Recommendation(
                user_id=user_id,
                stock_id=stock.id,
                action=action,
                confidence=round(confidence, 2),
                predicted_trend="Uptrend" if expected_return > 0 else "Downtrend" if expected_return < 0 else "Neutral",
                stop_loss=0.90 if risk_level == "low" else 0.85,
                take_profit=1.15 if risk_level == "low" else 1.25,
                allocation=round(allocation * 100, 1) if allocation > 0 else 0,
                reason=f"ML prediction: {predicted_price:+.3f}. {stock.symbol} ({stock.sector}) aligns with {risk_level}-risk portfolio.",
                risk_explanation=risk_exp,
                strategy=strategy
            )
            
            db.add(recommendation)

            # ✅ FIXED: return JSON instead of ORM
            recommendations.append({
                "symbol": stock.symbol,
                "action": action,
                "confidence": round(confidence, 2),
                "trend": "Uptrend" if expected_return > 0 else "Neutral",
                "allocation": round(allocation * 100, 1)
            })
            
        except Exception as e:
            logger.error(f"Error generating recommendation for {stock.symbol}: {e}")
            continue
    
    db.commit()
    logger.info(f"Generated {len(recommendations)} recommendations for user {user_id} (risk: {risk_level})")
    
    return recommendations

def generate_recommendation(df, prediction):
    """
    Simple recommendation for pipeline (no DB, no user).
    Used for ML pipeline flow.
    """

    try:
        if df is None or df.empty:
            return "HOLD"

        current_price = df["close"].iloc[-1]
        predicted_price = prediction.get("predicted_price")

        if predicted_price is None:
            return "HOLD"

        # Basic logic
        if predicted_price > current_price * 1.02:
            return "BUY"
        elif predicted_price < current_price * 0.98:
            return "SELL"
        else:
            return "HOLD"

    except Exception as e:
        logger.error(f"Pipeline recommendation error: {e}")
        return "HOLD"