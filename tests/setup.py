"""Module containing tests setup."""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


ASYNC_TEST_DB_URL = "sqlite+aiosqlite:///database.db"
TEST_DB_URL = "sqlite:///database.db"

async_engine = create_async_engine(ASYNC_TEST_DB_URL, echo=True)
sync_engine = create_engine(TEST_DB_URL)

AsyncTestSession = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autocommit=False,
    class_=AsyncSession,
)
