import aiosqlite
import pytest
from sqlalchemy import insert

from src.db import Rate
from tests.setup import AsyncTestSession, async_engine


@pytest.fixture(scope="function")
async def db_session():
    """Use test db session."""
    connection = await async_engine.connect()
    await connection.begin()
    session = AsyncTestSession(bind=connection)
    yield session
    await session.close()
    await connection.close()


@pytest.fixture(scope="function")
async def db_sqlite_session():
    """Sqlite session."""
    async with aiosqlite.connect(":memory:") as db:
        yield db


@pytest.fixture(scope="function")
async def rates(db_session):
    """Rates fixture."""
    values = [
        {
            "name": "EUR",
            "code": "GBP",
            "rate": 10.8562,
        },
        {
            "name": "EUR",
            "code": "JPY",
            "rate": 16200.4894,
        },
        {
            "name": "EUR",
            "code": "USD",
            "rate": 100.0816,
        },
    ]
    stmt = insert(Rate).values(values)
    await db_session.execute(stmt)
    await db_session.commit()
