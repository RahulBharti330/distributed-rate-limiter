import asyncio
import uuid
from app.soft_throttle.queue import enqueue_request
from app.global_limiter.leaky_bucket import GlobalServerLimiter
from app.core.server_config import get_server_capacity
from app.core.metrics import metrics

global_limiter = GlobalServerLimiter()


async def try_soft_throttle() -> bool:
    request_id = str(uuid.uuid4())

    queued = await enqueue_request(request_id)
    if not queued:
        return False

    metrics.record_queued()

    await asyncio.sleep(1)  # MAX_WAIT_SECONDS

    capacity = await get_server_capacity()
    allowed = await global_limiter.allow(capacity)

    if allowed:
        metrics.record_delayed()
        return True

    return False
