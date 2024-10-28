from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_async_session
from core.db.repository import BaseRepository
from models import Category


class CategoryRepository(BaseRepository[Category, int]):
    """Repository for managing category-related queries"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Category, session)

async def get_category_repository(session: AsyncSession = Depends(get_async_session)) -> CategoryRepository:
    """Method for sending a session to CategoryRepository"""
    return CategoryRepository(session)
