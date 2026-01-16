import asyncio
import time
from app.rate_limiter.limiter import RateLimiter
from app.core.metrics import metrics
from app.simulator.fake_request import FakeRequest
from app.policy.engine import PolicyEngine

rate_limiter = RateLimiter()
policy_engine = PolicyEngine()


def build_fake_request(config):
    headers = {
        "X-User-Tier": config.user_tier,
        "X-User-Id": "sim-user"
    }
    return FakeRequest(headers=headers, path=config.endpoint)


async def start_simulation(config):
    """
    Start traffic simulation with GLOBAL RPS distributed evenly across users.
    """
    tasks = []

    for _ in range(config.users):
        tasks.append(simulate_single_user(config))

    await asyncio.gather(*tasks)


async def simulate_single_user(config):
    """
    Each user independently generates traffic at:
    global_rps / users
    """
    start_time = time.time()
    end_time = start_time + config.duration_seconds

    per_user_rps = config.requests_per_second / config.users

    # Guard against invalid input
    if per_user_rps <= 0:
        return

    interval = 1 / per_user_rps

    while time.time() < end_time:
        await simulate_single_request(config)
        await asyncio.sleep(interval)


async def simulate_single_request(config):
    fake_request = build_fake_request(config)

    policy = await policy_engine.get_policy(config.user_tier)

    result = await rate_limiter.check(
        request=fake_request,
        api_name=config.endpoint,
        policy=policy
    )

    if result.allowed:
        metrics.record_allowed()
    else:
        metrics.record_blocked()
