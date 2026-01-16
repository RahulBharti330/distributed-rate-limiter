from fastapi import Request


class RateLimiter:
    async def allow_request(self, request: Request, api_name: str) -> bool:
        """
        Decide whether a request should be allowed or rejected.
        """
        # Placeholder — logic implemented next
        return True
