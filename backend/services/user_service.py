from sqlalchemy.orm import Session
from backend.models.user import User
import logging

logger = logging.getLogger(__name__)

def get_user_by_id(db: Session, user_id: int):
    
    # ✅ Basic validation
    if not user_id:
        logger.warning("Invalid user_id provided")
        return None

    user = db.query(User).filter(User.id == user_id).first()

    # ✅ Logging for debugging (very useful in your project)
    if not user:
        logger.warning(f"User not found: {user_id}")
    else:
        logger.info(f"User fetched: {user.email}")

    return user