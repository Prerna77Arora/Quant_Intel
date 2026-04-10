from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from backend.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------
# PASSWORD FUNCTIONS
# -------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------
# TOKEN FUNCTIONS
# -------------------------

def create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),  # ✅ added issued-at time
        "type": token_type         # ✅ token type (access/refresh)
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_access_token(user_id: int):
    return create_token(
        {"sub": str(user_id)},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )


def create_refresh_token(user_id: int):
    return create_token(
        {"sub": str(user_id)},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )


# -------------------------
# TOKEN VERIFY (SECURE)
# -------------------------

def verify_token(token: str, expected_type: str = "access"):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # ✅ Validate token type
        if payload.get("type") != expected_type:
            return None

        # ✅ Validate user ID
        user_id = payload.get("sub")
        if user_id is None:
            return None

        return payload

    except JWTError:
        return None