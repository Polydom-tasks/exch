"""Module containing client to interact with exchangerates api."""

from __future__ import annotations

import httpx
from httpx import AsyncClient
from pydantic import BaseModel

from core.config import settings


class RatesResponse(BaseModel):
    """Response from exch client latest rates request."""

    success: bool
    timestamp: int
    base: str
    date: str
    rates: dict[str, float]


class Error(BaseModel):
    """Error data."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Response from exch client if error occurred."""

    error: Error


class ExchClient:
    """Client to interact with api."""

    def __init__(self) -> None:
        """Construct client with base url and api key."""
        self.base_url = settings.EXCH_BASE_URL
        self.api_key = settings.EXCH_ACCESS_KEY

    async def get_rates(self, symbols: str) -> tuple[bool, RatesResponse | ErrorResponse]:
        """Fetch rates from api."""
        path = f"{self.base_url}/latest?access_key={self.api_key}&base=EUR&symbols={symbols}"
        async with AsyncClient() as client:
            response = await client.get(path)

        if response.status_code != httpx.codes.OK:
            return True, ErrorResponse.parse_obj(response.json())

        return False, RatesResponse.parse_obj(response.json())
