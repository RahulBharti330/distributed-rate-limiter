import time
from fastapi import Request
from app.core.redis import get_redis
from app.rate_limiter.identifier import identify_request
from pathlib import Path
from loguru import logger


class RateLimitResult:
    def __init__(self, allowed: bool, remaining: int, retry_after: int | None):
        self.allowed = allowed
        self.remaining = remaining
        self.retry_after = retry_after


class RateLimiter:
    def __init__(self):
        self.capacity = 10
        self.refill_rate = 1
        self.lua_script = self._load_lua_script()

    def _load_lua_script(self) -> str:
        script_path = Path(__file__).parent / "token_bucket.lua"
        return script_path.read_text()

    async def check(self, request: Request, api_name: str) -> RateLimitResult:
        redis = await get_redis()
        identifier = await identify_request(request)
        key = f"rate_limit:{identifier}:{api_name}"

        now = int(time.time())

        allowed, remaining = await redis.eval(
            self.lua_script,
            1,
            key,
            self.capacity,
            self.refill_rate,
            now
        )

        logger.info(f"Rate limit decision → allowed={allowed}, remaining={remaining}")

        retry_after = None
        if not allowed:
            retry_after = int(1 / self.refill_rate)

        return RateLimitResult(
            allowed=allowed == 1,
            remaining=max(0, int(remaining)),
            retry_after=retry_after
        )
