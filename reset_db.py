#!/usr/bin/env python3
"""
Database Reset Script - Drops and recreates all tables
Run this to sync database schema with current models
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.database import Base, engine
from backend.models.user import User
from backend.models.stock import Stock
from backend.models.recommendation import Recommendation
from backend.models.chatbot import ChatbotSession, ChatMessage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """Drop all tables and recreate them"""
    try:
        logger.info("🔄 Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ All tables dropped")
        
        logger.info("🔄 Creating all tables from models...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ All tables created successfully")
        
        logger.info("\n📊 Created tables:")
        logger.info("  - users")
        logger.info("  - stocks")
        logger.info("  - recommendations")
        logger.info("  - chatbot_sessions")
        logger.info("  - chat_messages")
        
        logger.info("\n✨ Database reset complete!")
        logger.info("You can now register and login.")
        
    except Exception as e:
        logger.error(f"❌ Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════╗
║     TradeMind Database Reset Tool      ║
╚════════════════════════════════════════╝
    """)
    
    confirm = input("⚠️  This will DROP ALL DATA. Continue? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        reset_database()
    else:
        print("❌ Cancelled")
        sys.exit(0)
