"""Module containing rates model."""

from sqlalchemy import DECIMAL, Column, DateTime, Integer, String, func

from . import Base


class Rate(Base):
    """Exchange rates table."""

    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(3), nullable=False)
    code = Column(String(3), nullable=False, unique=True)
    rate = Column(DECIMAL(10, 4), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
