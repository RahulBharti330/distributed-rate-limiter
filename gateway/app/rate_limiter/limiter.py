import time
from pathlib import Path
from fastapi import Request
from loguru import logger

from app.core.redis import get_redis
from app.rate_limiter.identifier import identify_request


class RateLimitResult:
    def __init__(self, allowed: bool, remaining: int, retry_after: int | None, limit: int):
        self.allowed = allowed
        self.remaining = remaining
        self.retry_after = retry_after
        self.limit = limit



class RateLimiter:
    def __init__(self):
        self.lua_script = self._load_lua_script()

    def _load_lua_script(self) -> str:
        script_path = Path(__file__).parent / "token_bucket.lua"
        return script_path.read_text()

    async def check(self, request: Request, api_name: str, policy: dict) -> RateLimitResult:
        redis = await get_redis()
        identifier = await identify_request(request)
        key = f"rate_limit:{identifier}:{api_name}"

        capacity = policy["capacity"]
        refill_rate = policy["refill_rate"]
        now = int(time.time())

        allowed, remaining = await redis.eval(
            self.lua_script,
            1,
            key,
            capacity,
            refill_rate,
            now
        )

        retry_after = None
        if not allowed:
            retry_after = int(1 / refill_rate)

        return RateLimitResult(
            allowed=allowed == 1,
            remaining=max(0, int(remaining)),
            retry_after=retry_after,
            limit=capacity
        )
