"""Module containing usecase to get existing rates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.repositories.rates import RateModel


class RatesRepositoryInterface(Protocol):
    """Rate repository."""

    async def get(self) -> list[RateModel]:
        """Get rates."""
        raise NotImplementedError


@dataclass
class GetRatesUsecase:
    """Fetch rates from db."""

    repository: RatesRepositoryInterface

    async def get(self) -> list[RateModel]:
        """Get rates."""
        return await self.repository.get()
