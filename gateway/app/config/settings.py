from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Distributed Rate Limiter Gateway"

    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        env_file = ".env"


settings = Settings()
