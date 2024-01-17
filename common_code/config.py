from enum import Enum
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TEST = "test"


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")

    engine_urls: List[str] = ["http://localhost:8080"]
    service_url: str = "http://localhost:9090"
    environment: Environment = Environment.DEVELOPMENT
    max_tasks: int = 50
    log_level: LogLevel = LogLevel.DEBUG
    engine_announce_retries: int = 5
    engine_announce_retry_delay: int = 3


@lru_cache()
def get_settings():
    return Settings()
