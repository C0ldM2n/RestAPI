from pydantic import BaseModel

from core.db.repository import ID, Model
from core.db.repository.base_repository import BaseRepository
from core.utils.cycle_checker import ensure_no_cycle


class HierarchicalRepository(BaseRepository[Model, ID]):
    """Repository for hierarchical models that adds cycle checking."""

    async def update(self, pk: ID, data: BaseModel) -> Model:
        """We override update to add a check."""
        payload = data.model_dump(exclude_unset=True)

        if "parent_id" in payload:
            await ensure_no_cycle(
                session=self._session,
                model=self._model,
                object_id=pk,
                new_parent_id=payload.get("parent_id"),
            )

        obj = await self._session.get(self._model, pk)
        for field, value in payload.items():
            setattr(obj, field, value)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj
