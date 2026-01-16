import time
from app.core.redis import get_redis

class GlobalServerLimiter:
    def __init__(self):
        self.key = "global_server_capacity"

    async def allow(self, max_rps: int) -> bool:
        """
        Returns True if request can be forwarded to backend.
        """
        redis = await get_redis()
        now = int(time.time())

        lua_script = """
        local key = KEYS[1]
        local max_rps = tonumber(ARGV[1])
        local now = tonumber(ARGV[2])

        local data = redis.call("HMGET", key, "current", "last_ts")
        local current = tonumber(data[1]) or 0
        local last_ts = tonumber(data[2]) or now

        -- leak tokens based on time passed
        local elapsed = now - last_ts
        current = math.max(0, current - elapsed * max_rps)

        if current + 1 > max_rps then
            redis.call("HMSET", key, "current", current, "last_ts", now)
            return 0
        end

        current = current + 1
        redis.call("HMSET", key, "current", current, "last_ts", now)
        return 1
        """

        allowed = await redis.eval(
            lua_script,
            1,
            self.key,
            max_rps,
            now
        )

        return allowed == 1
