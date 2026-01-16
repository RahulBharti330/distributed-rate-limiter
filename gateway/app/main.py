from fastapi import FastAPI
from app.api.health import router as health_router
from app.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(title="Distributed Rate Limiter Gateway")

app.add_middleware(RateLimitMiddleware)
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "API Gateway is running"}
