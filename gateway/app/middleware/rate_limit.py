from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.rate_limiter.limiter import RateLimiter
from app.core.metrics import metrics

rate_limiter = RateLimiter()

EXCLUDED_PATHS = ("/health", "/admin")


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 🔹 Exclude control-plane endpoints
        if path.startswith(EXCLUDED_PATHS):
            return await call_next(request)

        api_name = path
        result = await rate_limiter.check(request, api_name)

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

        response.headers["X-RateLimit-Limit"] = str(rate_limiter.capacity)
        response.headers["X-RateLimit-Remaining"] = str(result.remaining)

        return response
