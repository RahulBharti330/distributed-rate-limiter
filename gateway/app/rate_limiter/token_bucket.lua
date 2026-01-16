-- KEYS[1] = rate limit key
-- ARGV[1] = capacity
-- ARGV[2] = refill_rate (tokens per second)
-- ARGV[3] = current timestamp (seconds)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local data = redis.call("HMGET", key, "tokens", "last_refill_ts")
local tokens = tonumber(data[1])
local last_refill_ts = tonumber(data[2])

if tokens == nil then
    tokens = capacity
    last_refill_ts = now
end

local elapsed = math.max(0, now - last_refill_ts)
local refill = elapsed * refill_rate
tokens = math.min(capacity, tokens + refill)

local allowed = 0
if tokens >= 1 then
    allowed = 1
    tokens = tokens - 1
end

redis.call("HMSET", key,
    "tokens", tokens,
    "last_refill_ts", now
)

local ttl = math.max(1, math.ceil(capacity / refill_rate))
redis.call("EXPIRE", key, ttl)

return { allowed, tokens }