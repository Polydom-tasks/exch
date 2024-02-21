"""Package containing db configs and models."""

from src.database import Base

from .rates import Rate

__all__ = [
    "Base",
    "Rate",
]
