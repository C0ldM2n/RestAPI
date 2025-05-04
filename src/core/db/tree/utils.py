from typing import TypeVar, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.schema import Table
from sqlalchemy.ext.asyncio import AsyncSession

ID = TypeVar("ID", bound=Union[UUID, int])


async def is_descendant_of(
    session: AsyncSession, instance, ancestor_id: int, table: Table
) -> bool:
    """Check if the current instance is a descendant of a given ancestor ID."""
    current = instance
    while current.parent_id is not None:
        if current.parent_id == ancestor_id:
            return True
        result = await session.execute(
            select(table).filter_by(id=current.parent_id)
        )
        current = result.scalar_one_or_none()
        if current is None:
            break
    return False


# async def validate_no_cycles(self, node_id: ID, parent_id: ID) -> None:
#     """Ensure there are no cyclic references in the hierarchy."""
#     current_parent_id = parent_id
#     while current_parent_id is not None:
#         if current_parent_id == node_id:
#             raise ValueError("Cyclic reference detected in the hierarchy.")
#         current_parent = await self.session.get(self.model, current_parent_id)
#         if current_parent is None:
#             break
#         current_parent_id = current_parent.parent_id


async def validate_no_cycless(self, pk: ID, new_parent_id: ID) -> None:
    """Ensure there are no cyclic references in the hierarchy."""
    query = select(self.model.parent_id).where(new_parent_id == self.model.id)
    parent = await self.session.execute(query)
    if parent == pk:
        raise ValueError("Cyclic reference detected in the hierarchy.")
    else:
        pass

    # while old_parent_id is not None:
    #     if old_parent_id == pk:
    #         raise ValueError("Cyclic reference detected in the hierarchy.")
    #     current_parent = await self.session.get(self.model, old_parent_id)
    #     if current_parent is None:
    #         break  # Parent doesn't exist (which is fine), so break the loop
    #     old_parent_id = getattr(current_parent, parent_id_attr_name)
