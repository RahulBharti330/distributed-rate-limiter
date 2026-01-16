from app.core.redis import get_redis

SERVER_CAPACITY_KEY = "server_max_rps"

async def get_server_capacity() -> int:
    redis = await get_redis()
    value = await redis.get(SERVER_CAPACITY_KEY)
    return int(value) if value else 100  # default

async def set_server_capacity(rps: int):
    redis = await get_redis()
    await redis.set(SERVER_CAPACITY_KEY, rps)
