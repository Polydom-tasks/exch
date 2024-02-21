"""Module containing tests for set rates usecase."""

from dataclasses import dataclass
from typing import Callable

import pytest

from src.exch import ErrorResponse, RatesResponse
from src.repositories.rates import RatesRepository
from src.usecases.set_rates import SetRatesUsecase
from src.validators.symbols import SymbolsValidator

pytestmark = pytest.mark.slow


@dataclass
class FakeExchClient:
    """Fake implementation of exch client."""

    rates_factory: Callable[[], dict[str, float]]

    async def get_rates(self, symbols: str) -> tuple[bool, RatesResponse | ErrorResponse]:
        """Fetch rates from api."""
        return False, RatesResponse(
            success=True,
            timestamp=1519296206,
            base="EUR",
            date="2021-03-17",
            rates=self.rates_factory(),
        )


class FakeRateRepository:
    """Fake rates repository."""

    async def bulk_create_or_update(self, values: list[dict[str, str | float]]) -> None:
        """Create rates in db."""
        raise NotImplementedError


@pytest.mark.asyncio()
async def test_set_rates(db_session) -> None:
    """Test rates are set."""

    # Given: fake rates
    symbols = "GBP,USD,JPY"
    rates = {
        "GBP": 0.882047,
        "JPY": 132.360679,
        "USD": 1.23396,
    }

    # When: we try to set rates
    repo = RatesRepository(db_session)
    usecase = SetRatesUsecase(
        client=FakeExchClient(rates_factory=lambda: rates),
        validator=SymbolsValidator(symbols),
        repository=repo,
    )
    result = await usecase.set_rates(symbols)
    # Then: we check that result is successful
    assert result.success is True

    # Then: we check that rates are present in database
    db_rates = sorted(await repo.get(), key=lambda x: x.id)
    assert len(db_rates) == 3
    assert db_rates[0].code == "GBP"
    assert db_rates[0].rate == 0.882
