from sqlalchemy import select
from sqlalchemy.schema import Table
from sqlalchemy.ext.asyncio import AsyncSession

async def is_descendant_of(session: AsyncSession, instance, ancestor_id: int, table: Table) -> bool:
    """Check if the current instance is a descendant of a given ancestor ID."""
    current = instance
    while current.parent_id is not None:
        if current.parent_id == ancestor_id:
            return True
        result = await session.execute(select(table).filter_by(id=current.parent_id))
        current = result.scalar_one_or_none()
        if current is None:
            break
    return False
