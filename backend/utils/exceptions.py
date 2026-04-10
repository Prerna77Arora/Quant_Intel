from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging

# 🔧 Logger (important for debugging in production)
logger = logging.getLogger(__name__)


# 🌍 Global Exception Handler
async def global_exception_handler(request: Request, exc: Exception):
    
    # Log the error (VERY useful for debugging backend issues)
    logger.error(f"Error occurred: {str(exc)}")

    # Handle FastAPI HTTP exceptions separately
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    # Fallback for unknown errors
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"}
    )