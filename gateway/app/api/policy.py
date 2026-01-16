import json
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.redis import get_redis

router = APIRouter(prefix="/admin/policy", tags=["policy"])

class PolicyRequest(BaseModel):
    tier: str
    capacity: int
    refill_rate: int

@router.post("/update")
async def update_policy(req: PolicyRequest):
    redis = await get_redis()
    key = f"rate_policy:{req.tier}"

    await redis.set(
        key,
        json.dumps({
            "capacity": req.capacity,
            "refill_rate": req.refill_rate
        })
    )

    return {"status": "updated", "tier": req.tier}
