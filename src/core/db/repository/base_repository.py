from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.repository import Model, ID
from core.db.repository.interfaces import IRepository
from core.db.repository.error_converter import convert_db_errors
from core.utils.cycle_checker import ensure_no_cycle


class BaseRepository(IRepository[Model, ID]):
    def __init__(self, model: type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    @convert_db_errors()
    async def create(self, data: BaseModel) -> Model:
        payload = data.model_dump()
        instance = self._model(**payload)
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    @convert_db_errors()
    async def read(self, pk: ID) -> Model:
        obj = await self._session.get(self._model, pk)
        return obj

    @convert_db_errors()
    async def update(self, pk: ID, data: BaseModel) -> Model:
        payload = data.model_dump()
        obj = await self._session.get(self._model, pk)

        if "parent_id" in payload:
            await ensure_no_cycle(
                session=self._session,
                model=self._model,
                object_id=pk,
                new_parent_id=payload["parent_id"],
            )

        for field, value in payload.items():
            setattr(obj, field, value)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def delete(self, pk: ID) -> None:
        query = delete(self._model).where(pk == self._model.id)
        await self._session.execute(query)
        await self._session.commit()
        return None
