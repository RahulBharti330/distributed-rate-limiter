from fastapi import APIRouter
from app.core.redis import get_redis

router = APIRouter()


@router.get("/health")
async def health_check():
    redis = await get_redis()
    pong = await redis.ping()

    return {
        "status": "ok",
        "redis": pong
    }

