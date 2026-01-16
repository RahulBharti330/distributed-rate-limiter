import time
from app.core.redis import get_redis

QUEUE_KEY = "soft_throttle_queue"
MAX_QUEUE_SIZE = 100
MAX_WAIT_SECONDS = 1


async def enqueue_request(request_id: str) -> bool:
    redis = await get_redis()
    size = await redis.llen(QUEUE_KEY)

    if size >= MAX_QUEUE_SIZE:
        return False

    await redis.rpush(QUEUE_KEY, request_id)
    return True


async def dequeue_request() -> str | None:
    redis = await get_redis()
    return await redis.lpop(QUEUE_KEY)


async def queue_size() -> int:
    redis = await get_redis()
    return await redis.llen(QUEUE_KEY)
