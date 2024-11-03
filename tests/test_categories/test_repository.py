import json
from pathlib import Path

import pytest

from products.categories.schemas import CategoryCreateSchema
from products.categories.repository import CategoryRepository


# CategoryID = Annotated[int, Path(..., alias="id")]
# CategoryRepo = Annotated[CategoryRepository, Depends(get_category_repository)]


def load_category_data(filename: str = "./fake_data/categories.json") -> CategoryCreateSchema:
	"""Loads category data from a JSON file."""
	with open(Path(__file__).parent / filename, "r") as file:
		data = json.load(file)
	# Convert each dictionary to a CategoryCreate instance

	# category_data = [CategoryCreate(**item) for item in data]
	return data


class TestRepository:

	@pytest.fixture(autouse=True)
	async def setup_method(self, db_session):
		"""Setup repository for each test with an active database session"""
		self.repo = CategoryRepository(db_session)
		self.data = load_category_data()

	# class TestCategoryCreate:
	async def test_create_category_success(self):
		# Take the first category from JSON as sample data
		# print(**self.data[0])

		data = self.data
		result = await self.repo.create(data)  # data[0] is now a CategoryCreate instance
		print(result)

		assert result is not None
		assert result.name == data["name"]

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

	# async def test_create_category_duplicate(self):
	# 	# Try creating the same category twice
	# 	data: list[CategoryCreate] = load_category_data
	#
	# 	category_data = CategoryCreate(**self.data[0])
	# 	await self.repo.create(data=category_data.model_dump())
	#
	# 	with pytest.raises(Exception):  # Adjust based on expected exception
	# 		await self.repo.create(data=category_data.model_dump())



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
