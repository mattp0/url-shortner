from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # core
    ENV: str = "dev"
    LOG_LEVEL: str = "info"

    # secrets / connections
    DATABASE_URL: str
    REDIS_URL: Optional[str] = None
    SECRET_KEY: str = "replace-me"

    # feature flags / limits (tweak as needed)
    ALLOWED_SCHEMES: str = "http,https"
    DENY_PRIVATE_CIDR: bool = True
    RATE_CREATE_PER_MIN: int = 10

    # pydantic-settings will read .env on import in local dev
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    # cached so repeated calls are cheap and stable, even with uvicorn reloads
    return Settings()
