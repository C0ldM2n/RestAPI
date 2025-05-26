from typing import Type

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import BaseModel
from core.db.database import get_async_session
from core.db.repository.base_repository import BaseRepository


class RepositoryFactory:
    @staticmethod
    def create(_model: Type[BaseModel], session: AsyncSession = Depends(get_async_session)):
        return BaseRepository(_model, session)
