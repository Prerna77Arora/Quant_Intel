from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.core.config import settings
import logging

logger = logging.getLogger(__name__)

# ✅ Get DB URL
DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# 🔥 Ensure SSL for Supabase
if "sslmode" not in DATABASE_URL:
    DATABASE_URL += "&sslmode=require" if "?" in DATABASE_URL else "?sslmode=require"

logger.info("Connecting to database...")

# ✅ Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False
)

# ✅ Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Base model
Base = declarative_base()