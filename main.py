from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from core.config import logging_conf, settings
from src.api import api_router

dictConfig(logging_conf)

openapi_url = f"{settings.API_V1_PATH}/openapi.json"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=openapi_url,
)

app.include_router(api_router, prefix=settings.API_V1_PATH)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="EXCH API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
