from typing import Type

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import BaseModel
from core.db.database import get_async_session
from core.db.repository.base_repository import BaseRepository


class RepositoryFactory:
    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    def __call__(self, model: Type[BaseModel]) -> BaseRepository:
        return BaseRepository(model, self._session)
