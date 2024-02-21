"""Module containing project settings."""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Project settings."""

    load_dotenv()

    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_NAME: str = os.getenv("POSTGRES_DB")
    DB_HOST: str = os.getenv("POSTGRES_HOST")

    POSTGRES_ASYNC_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

    API_V1_PATH: str = "/api/v1"
    PROJECT_NAME: str = "assessment"
    EXCH_BASE_URL: str = "http://api.exchangeratesapi.io/v1"
    EXCH_ACCESS_KEY: str = os.getenv("EXCH_ACCESS_KEY")


settings = Settings()

logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": True,
        },
    },
}
