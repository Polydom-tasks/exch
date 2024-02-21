"""Module containing usecase to collect rates from external api and store them in db."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from src.schemas import CommonResponse

if TYPE_CHECKING:
    from src.exch import ErrorResponse, RatesResponse


class ClientInterface(Protocol):
    """Interface for third party client."""

    async def get_rates(self, symbols: str) -> tuple[bool, RatesResponse | ErrorResponse]:
        """Fetch rates from api."""
        raise NotImplementedError


class ValidatorInterface(Protocol):
    """Validator interface."""

    async def is_valid(self) -> bool:
        """Validate."""
        raise NotImplementedError


class RatesRepositoryInterface(Protocol):
    """Rate repository."""

    async def bulk_create_or_update(self, values: list[dict[str, str | float]]) -> None:
        """Create rates in db."""
        raise NotImplementedError


@dataclass
class SetRatesUsecase:
    """
    Handle rates.

    Validate request
    Fetch rates from api.
    Store data in db.
    """

    client: ClientInterface
    validator: ValidatorInterface
    repository: RatesRepositoryInterface

    async def set_rates(self, symbols: str) -> CommonResponse:
        """Store fetched data in database."""
        is_valid = await self.validator.is_valid()
        if not is_valid:
            return CommonResponse(success=False, message="Symbols not valid. Enter values according to docs.")

        err, response = await self.client.get_rates(symbols)
        if err:
            return CommonResponse(success=False, code=response.error.code, message=response.error.message)
        if not response.success:
            return CommonResponse(success=False, message="Something went wrong when fetching data from external api.")

        await self.store_rates(response.rates)
        return CommonResponse(success=True, code=None, message="Successfully updated rates")

    async def store_rates(self, rates: dict[str, float]) -> None:
        """Store rates in database."""
        values = [{"name": "EUR", "code": code, "rate": rate} for code, rate in rates.items()]
        await self.repository.bulk_create_or_update(values)
