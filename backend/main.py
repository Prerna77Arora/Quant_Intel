from dotenv import load_dotenv
import os

load_dotenv()

# Debug (remove later)
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ USE ONLY ONE DATABASE (IMPORTANT)
from data_pipeline.database import Base, engine

from backend.core.log_config import setup_logging
from backend.routers import (
    auth,
    user,
    stock,
    recommendation,
    prediction,
    pipeline,
    chatbot
)
from backend.utils.exceptions import global_exception_handler


# ---------------------- INITIAL SETUP ---------------------- #
setup_logging()

app = FastAPI(
    title="TradeMind Backend",
    version="1.0.0",
    description="AI-powered stock prediction API"
)


# ---------------------- STARTUP EVENT ---------------------- #
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# ---------------------- CORS CONFIG ---------------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------- ROUTERS ---------------------- #
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(stock.router, prefix="/stocks", tags=["Stocks"])
app.include_router(recommendation.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(prediction.router, prefix="/prediction", tags=["Prediction"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])


# ---------------------- EXCEPTION HANDLER ---------------------- #
app.add_exception_handler(Exception, global_exception_handler)


# ---------------------- ROOT ENDPOINT ---------------------- #
@app.get("/")
def root():
    return {
        "message": "TradeMind API Running 🚀"
    }


# ---------------------- HEALTH CHECK ---------------------- #
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }