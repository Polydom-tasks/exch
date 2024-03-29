"""Tests config."""

import pytest

from src.database import Base
from .fixtures import db_session, db_sqlite_session, rates

__all__ = [
    "db_session",
    "db_sqlite_session",
]

from .setup import sync_engine


def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", default=False, help="run slow tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--slow"):
        # --slow given in cli: do not skip slow tests
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)
        return
    skip_slow = pytest.mark.skip(reason="need --slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
