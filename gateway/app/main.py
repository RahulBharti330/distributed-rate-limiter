from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.api.admin import router as admin_router
from app.middleware.rate_limit import RateLimitMiddleware
from app.api.user import router as user_router
from app.api.policy import router as policy_router
from app.api.simulator import router as simulator_router


app = FastAPI(title="Distributed Rate Limiter Gateway")

app.include_router(simulator_router)
app.include_router(user_router)
app.include_router(policy_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)

app.include_router(health_router)
app.include_router(admin_router)
