"""Module containing tests for converting rates."""

import pytest

from src.repositories.rates import RatesRepository
from src.usecases.convert import ConvertUsecase

pytestmark = pytest.mark.slow


@pytest.mark.asyncio()
async def test_convert_rates(db_session, rates) -> None:
    """Test convert rates."""

    # Given: rates from fixture

    # When: we try to convert rates
    repo = RatesRepository(db_session)
    usecase = ConvertUsecase(
        repository=repo,
    )
    result = await usecase.convert(source="JPY", target="GBP", amount=120000)

    # Then: we check that result is successful
    assert result.amount == 120000
    assert result.source == "JPY"
    assert result.target == "GBP"
    assert int(result.result) == 80


@pytest.mark.asyncio()
async def test_convert_rates_from_eur_to_gbp(db_session, rates) -> None:
    """Test convert rates."""

    # Given: rates from fixture

    # When: we try to convert rates
    repo = RatesRepository(db_session)
    usecase = ConvertUsecase(
        repository=repo,
    )
    result = await usecase.convert(source="EUR", target="GBP", amount=120000)

    # Then: we check that result is successful
    assert result.amount == 120000
    assert result.source == "EUR"
    assert result.target == "GBP"
    assert int(result.result) == 1302744
