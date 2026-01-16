from fastapi import APIRouter
from app.core.metrics import metrics
from pydantic import BaseModel
from app.core.server_config import set_server_capacity

router = APIRouter(prefix="/admin", tags=["admin"])

class ServerCapacityRequest(BaseModel):
    max_rps: int


@router.get("/metrics")
def get_metrics():
    return metrics.snapshot()

@router.post("/metrics/reset")
def reset_metrics():
    metrics.reset()
    return {"status": "metrics_reset"}


@router.post("/server-capacity")
async def update_server_capacity(req: ServerCapacityRequest):
    await set_server_capacity(req.max_rps)
    return {"status": "updated", "max_rps": req.max_rps}