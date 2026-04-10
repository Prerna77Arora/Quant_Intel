import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "TradeMind"

    # ✅ Database (Supabase PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # ✅ Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"

    # ✅ Token expiration
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    def validate(self):
        """Ensure required environment variables are set."""
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set")

        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set")


settings = Settings()
settings.validate()