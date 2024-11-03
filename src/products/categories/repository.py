import typing

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_async_session
from core.db.repository import BaseRepository
from models import Category


class CategoryRepository(BaseRepository[Category, int]):
	"""Repository for managing category-related queries"""

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

	@classmethod
	async def get_category_repository(cls, session: AsyncSession = Depends(get_async_session)):
		"""Method for sending a session to CategoryRepository"""
		return cls(Category, session)

async def get_repository(cls, session: AsyncSession = Depends(get_async_session)) -> typing.Type['CategoryRepository']:
	"""Method for sending a session to CategoryRepository"""
	return cls(Category, session)