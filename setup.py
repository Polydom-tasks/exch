"""Module containing script to produce initial data in db."""

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.db import Rate

SQLALCHEMY_DATABASE_URL = "postgresql://root:postgres@exch-db:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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


def init_db() -> None:
    """Init db data."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        stmt = insert(Rate).values(values)
        session.execute(stmt)
        session.commit()


if __name__ == "__main__":
    init_db()
