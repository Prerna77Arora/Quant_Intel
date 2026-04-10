from fastapi import APIRouter, HTTPException, status
from data_pipeline.run_pipeline import run

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


@router.post("/run", status_code=status.HTTP_200_OK)
def run_pipeline():
    """Trigger data pipeline execution."""
    try:
        result = run()

        return {
            "success": True,
            "data": result,
            "message": "Pipeline executed successfully"
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Pipeline execution failed"
        )