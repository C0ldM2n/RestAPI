import json
from pathlib import Path
from typing import Annotated, List
from unicodedata import category

import pytest
from http.client import responses

from fastapi import status, Depends
from httpx import AsyncClient
from sqlalchemy.orm import session
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_async_session
from core.db.repository import IntegrityConflictException, BaseRepository
from categories.schemas import CategoryCreate, CategoryPatch, CategoryPut
from categories.models import Category
from categories.repository import CategoryRepository, get_category_repository


# CategoryID = Annotated[int, Path(..., alias="id")]
# CategoryRepo = Annotated[CategoryRepository, Depends(get_category_repository)]


def load_category_data(filename: str = "./fake_data/categories.json") -> list[CategoryCreate]:
	"""Loads category data from a JSON file."""
	with open(Path(__file__).parent / filename, "r") as file:
		data = json.load(file)
	# Convert each dictionary to a CategoryCreate instance

	# category_data = [CategoryCreate(**item) for item in data]
	# print(category_data)
	print(data)
	return data


class TestRepository:

	# def __init__(self):
	# 	self.data = None
	# 	self.repo = None

	@pytest.fixture(autouse=True)
	async def setup_method(self, db_session):
		"""Setup a repository for each test with an active database session."""
		self.repo = CategoryRepository(db_session)
		self.data = load_category_data()

	# class TestCategoryCreate:
	async def test_create_category_success(self):
		# Take the first category from JSON as sample data
		# print(**self.data[0])

		data: list[CategoryCreate] = load_category_data()
		result = await CategoryRepository.create(data)  # data[0] is now a CategoryCreate instance

		assert result is not None
		assert result.name == data[0].name

		# category_data = CategoryCreate(**self.data[0]) if isinstance(self.data, list) else CategoryCreate(**self.data)
		# created_category = await self.repo.create(data=category_data.model_dump())
		# category_data = CategoryCreate(**self.data[0])
		# created_category = await self.repo.create(data=category_data.model_dump())




		# for category_data in load_category_data():
		# 	created_category = await CategoryRepo.create(category_data)
		#
		# 	# Assertions to ensure data integrity
		# 	assert created_category.name == category_data["name"]
		# 	assert created_category.is_active == category_data["is_active"]

		# category_data = load_category_data()[0]
		# new_category = await CategoryRepo.create(category_data)
		# for category_data in load_category_data():
		# 	new_category = await CategoryRepo.create(category_data)
		# assert new_category.id is not None
		# assert new_category.name == category_data["name"]

	async def test_create_category_duplicate(self):
		# Try creating the same category twice
		data: list[CategoryCreate] = load_category_data()

		category_data = CategoryCreate(**self.data[0])
		await self.repo.create(data=category_data.model_dump())

		with pytest.raises(Exception):  # Adjust based on expected exception
			await self.repo.create(data=category_data.model_dump())



# class TestCategoryGet:
# 	async def category_get_by_id(self):
#
#
#
# class TestCategoryPatch:
# 	async def category_patch(self):
#
#
#
# class TestCategoryPut:
# 	async def category_put(self):
#
#
#
# class TestCategoryDelete:
# 	async def category_delete(self):
