from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.rate_limiter.limiter import RateLimiter

rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_name = request.url.path

        allowed = await rate_limiter.allow_request(request, api_name)
        if not allowed:
            return Response(
                content="Too Many Requests",
                status_code=429
            )

        response = await call_next(request)
        return response
