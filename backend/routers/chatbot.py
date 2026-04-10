from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.utils.dependencies import get_current_user, get_db
from backend.services.chatbot_service import (
    create_chatbot_session,
    get_current_question,
    process_chatbot_response,
    get_active_session,
    save_chat_message,
    CHATBOT_STEPS
)
from backend.schemas.chatbot import ChatbotStepRequest
from backend.models.chatbot import ChatbotSession  # ✅ FIXED IMPORT

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/start")
def start_chatbot_session(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Start or resume chatbot session."""
    try:
        if getattr(user, "profile_complete", False):
            return {
                "success": True,
                "message": "Profile already complete",
                "completed": True
            }

        session = get_active_session(db, user.id)
        question = get_current_question(session)

        return {
            "success": True,
            "data": {
                "session_id": session.id,
                "current_step": session.current_step,
                "total_steps": len(CHATBOT_STEPS),
                "question": question["question"],
                "options": question["options"]
            }
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start chatbot session"
        )


@router.post("/step/{session_id}")
def process_chatbot_step(
    session_id: int,
    request: ChatbotStepRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Process chatbot answer."""
    try:
        # ✅ FIXED: proper model query (not string)
        session = db.query(ChatbotSession).filter(
            ChatbotSession.id == session_id,
            ChatbotSession.user_id == user.id
        ).first()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Save user response
        save_chat_message(db, user.id, session_id, "user", request.response)

        # Process logic
        result = process_chatbot_response(
            db, session_id, user.id, request.response, request.step
        )

        if not result["success"]:
            return result

        # If completed
        if result.get("completed"):
            save_chat_message(db, user.id, session_id, "bot", "Profile complete")
            return {
                "success": True,
                "completed": True,
                "message": result["message"]
            }

        # Get next question
        session = db.query(ChatbotSession).filter(
            ChatbotSession.id == session_id
        ).first()

        next_q = get_current_question(session)

        save_chat_message(db, user.id, session_id, "bot", next_q["question"])

        return {
            "success": True,
            "completed": False,
            "current_step": result["current_step"],
            "question": next_q["question"],
            "options": next_q["options"]
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error processing chatbot step"
        )


@router.get("/status/{session_id}")
def get_chatbot_status(
    session_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Get chatbot progress."""
    try:
        session = db.query(ChatbotSession).filter(
            ChatbotSession.id == session_id,
            ChatbotSession.user_id == user.id
        ).first()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        question = get_current_question(session)

        return {
            "success": True,
            "data": {
                "session_id": session.id,
                "current_step": session.current_step,
                "total_steps": len(CHATBOT_STEPS),
                "completed": session.completed,
                "question": question.get("question"),
                "options": question.get("options")
            }
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error fetching chatbot status"
        )