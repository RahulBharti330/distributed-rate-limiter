from app.core.redis import get_redis
import json

class PolicyEngine:
    async def get_policy(self, tier: str) -> dict:
        redis = await get_redis()   # 🔑 IMPORTANT
        key = f"policy:{tier}"

        data = await redis.get(key)

        if data:
            return json.loads(data)

        # default policy fallback
        policy = {
            "capacity": 10,
            "refill_rate": 5
        }

        await redis.set(key, json.dumps(policy))
        return policy
