import json
from app.core.redis import get_redis

DEFAULT_POLICIES = {
    "free": {"capacity": 10, "refill_rate": 1},
    "premium": {"capacity": 100, "refill_rate": 50},
    "enterprise": {"capacity": 500, "refill_rate": 200},
}

class PolicyEngine:
    async def get_policy(self, tier: str) -> dict:
        redis = await get_redis()
        key = f"rate_policy:{tier}"

        data = await redis.get(key)
        if data:
            return json.loads(data)

        # fallback default (safe)
        return DEFAULT_POLICIES.get(tier, DEFAULT_POLICIES["free"])
