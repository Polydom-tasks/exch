"""Module containing usecase to convert."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from src.schemas import ConvertResponse

if TYPE_CHECKING:
    from src.repositories.rates import RateModel


class RatesRepositoryInterface(Protocol):
    """Rate repository."""

    async def get(self) -> list[RateModel]:
        """Get rates."""
        raise NotImplementedError


SOURCE_TARGET_LEN = 2


@dataclass
class ConvertUsecase:
    """Usecase responsible for converting given amount from source to target rate."""

    repository: RatesRepositoryInterface

    async def convert(self, source: str, target: str, amount: float) -> ConvertResponse:
        """Handle convert request."""
        rates = await self.repository.get()
        source_target_rates = [rate for rate in rates if rate.code.lower() in (source.lower(), target.lower())]
        if len(source_target_rates) != SOURCE_TARGET_LEN:
            msg = "Symbols not valid. Enter values according to docs."
            raise ValueError(msg)

        source_rate, target_rate = source_target_rates
        if source_rate.code.lower() != source.lower():
            source_rate, target_rate = target_rate, source_rate

        result = await self.convert_amount(source_rate, target_rate, amount)
        return ConvertResponse(
            source=source,
            target=target,
            amount=amount,
            result=result,
        )

    async def convert_amount(self, source: RateModel, target: RateModel, amount: float) -> float:
        """Convert amount."""
        return amount / source.rate * target.rate
