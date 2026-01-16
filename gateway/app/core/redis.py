import os
import redis.asyncio as redis
from loguru import logger

_redis = None

async def get_redis():
    global _redis
    if _redis is None:
        redis_url = os.getenv("REDIS_URL")

        if not redis_url:
            raise RuntimeError("REDIS_URL is not set")

        _redis = redis.from_url(
            redis_url,
            decode_responses=True
        )

        logger.info("Connected to Redis")

    return _redis
