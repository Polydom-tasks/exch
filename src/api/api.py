"""Module containing router for project endpoints."""

from fastapi import APIRouter

from src.api import rates

api_router = APIRouter()

api_router.include_router(rates.router)
