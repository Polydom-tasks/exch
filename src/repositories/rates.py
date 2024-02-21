"""Module containing rates repository."""

from __future__ import annotations

import dataclasses
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, parse_obj_as
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from src.db.rates import Rate

if TYPE_CHECKING:

    from sqlalchemy.ext.asyncio import AsyncSession


class RateModel(BaseModel):
    """Rate model."""

    id: int
    name: str
    code: str
    rate: float
    created_at: datetime
    updated_at: datetime

    class Config:
        """Set orm mode."""

        from_attributes = True


@dataclasses.dataclass
class RatesRepository:
    """Repository responsible for interacting with rates table."""

    session: AsyncSession

    async def bulk_create_or_update(self, values: list[dict[str, str | float]]) -> None:
        """Create rates."""
        stmt = insert(Rate).values(values)

        stmt = stmt.on_conflict_do_update(
            index_elements=[Rate.code],
            set_={"rate": stmt.excluded.rate, "updated_at": func.now()},
        ).returning(Rate)
        await self.session.execute(stmt)
        await self.session.commit()
        await self.session.close()

    async def get(self) -> list[RateModel]:
        """Get rates."""
        stmt = select(Rate)
        query = await self.session.execute(stmt)
        await self.session.close()

        return parse_obj_as(list[RateModel], query.scalars().all())
