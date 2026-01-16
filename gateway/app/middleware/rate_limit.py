from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.rate_limiter.limiter import RateLimiter
from app.core.metrics import metrics
from app.global_limiter.leaky_bucket import GlobalServerLimiter
from app.core.server_config import get_server_capacity
from app.soft_throttle.handler import try_soft_throttle
from app.policy.engine import PolicyEngine



rate_limiter = RateLimiter()

EXCLUDED_PATHS = ("/health", "/admin")

global_limiter = GlobalServerLimiter()

policy_engine = PolicyEngine()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 🔹 Exclude control-plane endpoints
        if path.startswith(EXCLUDED_PATHS):
            return await call_next(request)

        tier = request.headers.get("X-User-Tier", "free")
        policy = await policy_engine.get_policy(tier)

        result = await rate_limiter.check(
            request=request,
            api_name=request.url.path,
            policy=policy
        )


        if not result.allowed:
            metrics.record_blocked()
            return Response(
                content="Too Many Requests",
                status_code=429,
                headers={
                    "X-RateLimit-Limit": str(rate_limiter.capacity),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": str(result.retry_after),
                },
            )

        metrics.record_allowed()
        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(result.limit)
        response.headers["X-RateLimit-Remaining"] = str(result.remaining)

        if not result.allowed and result.retry_after:
            response.headers["Retry-After"] = str(result.retry_after)


        # after user-level rate limit passes
        server_capacity = await get_server_capacity()

        server_allowed = await global_limiter.allow(server_capacity)

        if not server_allowed:
            soft_allowed = await try_soft_throttle()

            if not soft_allowed:
                metrics.record_server_reject()
                return Response(
                    content="Server overloaded",
                    status_code=503
                )



        return response
