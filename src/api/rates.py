"""Module containing endpoints to set rates."""

from __future__ import annotations

from fastapi import APIRouter
from starlette import status

from src.db.db_session import AsyncSessionLocal
from src.exch import ExchClient
from src.repositories.rates import RateModel, RatesRepository
from src.schemas import CommonResponse, ConvertRequest, ConvertResponse
from src.usecases.convert import ConvertUsecase
from src.usecases.get_rates import GetRatesUsecase
from src.usecases.set_rates import SetRatesUsecase
from src.validators.symbols import SymbolsValidator

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Update rates. Pass symbols in query params to store required rates. Ex: 'GBP,JPY,USD'",
)
async def set_rates(
    symbols: str = "GBP,JPY,USD",
) -> CommonResponse:
    """Endpoint to store rates in database."""
    usecase = SetRatesUsecase(
        client=ExchClient(),
        validator=SymbolsValidator(symbols=symbols),
        repository=RatesRepository(session=AsyncSessionLocal()),
    )
    return await usecase.set_rates(symbols)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Fetch rates",
)
async def get_rates() -> list[RateModel]:
    """Endpoint to fetch rates in database."""
    usecase = GetRatesUsecase(
        repository=RatesRepository(session=AsyncSessionLocal()),
    )
    return await usecase.get()


@router.post(
    "/convert",
    status_code=status.HTTP_200_OK,
    description="Convert amount from source to target",
)
async def convert(data: ConvertRequest) -> ConvertResponse:
    """Endpoint to convert amount from source to target."""
    usecase = ConvertUsecase(
        repository=RatesRepository(session=AsyncSessionLocal()),
    )
    return await usecase.convert(
        source=data.source,
        target=data.target,
        amount=data.amount,
    )
