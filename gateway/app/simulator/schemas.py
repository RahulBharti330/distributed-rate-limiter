from pydantic import BaseModel

class SimulationConfig(BaseModel):
    requests_per_second: int
    duration_seconds: int
    users: int
    endpoint: str
    user_tier: str
from pydantic import BaseModel

class SimulationConfig(BaseModel):
    requests_per_second: int
    duration_seconds: int
    users: int
    endpoint: str
    user_tier: str
