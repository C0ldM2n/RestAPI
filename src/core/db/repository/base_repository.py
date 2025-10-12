from functools import cached_property
from typing import get_args

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.repository import ID, Model
from core.db.repository.interfaces import IRepository


class BaseRepository(IRepository[Model, ID]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    @cached_property
    def _model(self) -> type[Model]:
        """Automatically determines the SQLAlchemy model via Generic type."""
        generic_base = self.__class__.__orig_bases__[0]
        return get_args(generic_base)[0]

    async def create(self, data: BaseModel) -> Model:
        payload = data.model_dump()
        instance = self._model(**payload)
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def read(self, pk: ID) -> Model:
        obj = await self._session.get(self._model, pk)
        return obj

    async def update(self, pk: ID, data: BaseModel) -> Model:
        payload = data.model_dump()
        obj = await self._session.get(self._model, pk)

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
