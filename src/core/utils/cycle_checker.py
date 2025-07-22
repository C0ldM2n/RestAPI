from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from core.db.repository import Model, ID


async def ensure_no_cycle(
    session: AsyncSession,
    model: type[Model],
    object_id: ID,
    new_parent_id: ID,
):
    if new_parent_id is None:
        return

    if object_id == new_parent_id:
        raise HTTPException(
            status_code=400,
            detail="Object cannot be as own parent.",
        )

    ancestor = aliased(model)

    cte = (
        select(model.id, model.parent_id)
        .where(model.id == new_parent_id)
        .cte(name="ancestors", recursive=True)
    )

    parent = aliased(cte)

    cte = cte.union_all(
        select(ancestor.id, ancestor.parent_id).join(
            parent, ancestor.id == parent.c.parent_id
        )
    )

    query = select(cte.c.id).where(cte.c.id == object_id)

    result = await session.execute(query)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Cycle reference: item cannot be as own children.",
        )
