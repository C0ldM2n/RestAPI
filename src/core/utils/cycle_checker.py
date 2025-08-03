from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.repository import Model, ID
from core.exceptions.base import CyclicReferenceError, SelfParentError


async def ensure_no_cycle(
    session: AsyncSession,
    model: type[Model],
    object_id: ID,
    new_parent_id: ID,
) -> None:
    """Checking for an inherited cycle in a table."""

    if new_parent_id is None:
        return

    elif object_id == new_parent_id:
        raise SelfParentError

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
        raise CyclicReferenceError
