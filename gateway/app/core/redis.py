from redis.asyncio import Redis
from loguru import logger
from app.config.settings import settings

redis_client: Redis | None = None


async def get_redis() -> Redis:
    global redis_client
    if redis_client is None:
        redis_client = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )
        logger.info("Connected to Redis")
    return redis_client
