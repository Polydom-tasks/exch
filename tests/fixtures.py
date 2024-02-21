import aiosqlite
import pytest

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
