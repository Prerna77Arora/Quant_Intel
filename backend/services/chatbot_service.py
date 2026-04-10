from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.chatbot import ChatbotSession, ChatMessage
from backend.models.user import User
import logging

logger = logging.getLogger(__name__)

CHATBOT_STEPS = {
    0: {
        "question": "What is your risk tolerance?",
        "options": ["Low", "Medium", "High"],
        "field": "risk_level"   # ✅ FIXED
    },
    1: {
        "question": "What is your budget?",
        "options": [],
        "field": "budget"
    },
    2: {
        "question": "Investment horizon?",
        "options": ["Short", "Medium", "Long"],
        "field": "investment_horizon"
    }
}


def create_chatbot_session(db: Session, user_id: int):
    session = ChatbotSession(user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_active_session(db: Session, user_id: int):
    session = db.query(ChatbotSession).filter(
        ChatbotSession.user_id == user_id,
        ChatbotSession.completed == False
    ).first()

    if not session:
        session = create_chatbot_session(db, user_id)

    return session


def get_current_question(session: ChatbotSession):
    step = session.current_step
    return CHATBOT_STEPS.get(step, {"question": "Profile completed 🎉", "options": []})


def process_chatbot_response(db: Session, session_id: int, user_id: int, response: str):
    session = db.query(ChatbotSession).filter(
        ChatbotSession.id == session_id
    ).first()

    user = db.query(User).filter(User.id == user_id).first()

    if not session or not user:
        raise HTTPException(status_code=404, detail="Session/User not found")

    step = session.current_step

    # ✅ Save user message
    save_chat_message(db, user_id, session_id, "user", response)

    try:
        if step == 0:
            if response.lower() not in ["low", "medium", "high"]:
                raise ValueError("Invalid risk level")
            user.risk_level = response.lower()

        elif step == 1:
            user.budget = float(response)

        elif step == 2:
            if response.lower() not in ["short", "medium", "long"]:
                raise ValueError("Invalid horizon")
            user.investment_horizon = response.lower()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ✅ Move to next step
    session.current_step += 1

    # ✅ Completion logic
    if session.current_step >= len(CHATBOT_STEPS):
        session.completed = True
        user.profile_complete = True

        save_chat_message(
            db, user_id, session_id, "assistant",
            "Your investment profile is ready 🎯"
        )

    else:
        next_q = CHATBOT_STEPS[session.current_step]["question"]

        save_chat_message(
            db, user_id, session_id, "assistant",
            next_q
        )

    db.commit()

    return {
        "success": True,
        "completed": session.completed,
        "current_step": session.current_step,
        "next_question": get_current_question(session)
    }


def save_chat_message(db: Session, user_id: int, session_id: int, role: str, content: str):
    msg = ChatMessage(
        user_id=user_id,
        session_id=session_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()