from fastapi import APIRouter
from app.core.metrics import metrics

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/metrics")
def get_metrics():
    return metrics.snapshot()
