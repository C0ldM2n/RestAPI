import uuid
from typing import Generic, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select, delete, BinaryExpression
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (CategoryNotFounded, CategoryUnprocessableEntity,
                             ValidationError, DatabaseIntegrityError, UnexpectedError)

"""Type variables for BaseRepository"""
# Table model
Model = TypeVar("Model")
# Flexible ID type (int and uuid)
ID = TypeVar("ID", bound=Union[uuid.UUID, int])


class BaseRepository(Generic[Model, ID]):
	"""Generic repository for performing database queries with flexible ID types"""

	def __init__(self, model: type[Model], session: AsyncSession) -> None:
		"""Initialize with model and session"""
		self.model = model
		self.session = session

	async def _execute_with_error_handling(self, func, *args, **kwargs):
		"""Helper method to handle exceptions within repository functions"""
		try:
			return await func(*args, **kwargs)
		except IntegrityError as e:
			# Database integrity error handling
			await self.session.rollback()
			raise DatabaseIntegrityError(str(e))
		except ValueError as e:
			# Validating values error handling
			raise ValidationError(str(e))
		except Exception as e:
			# Generic error handling
			await self.session.rollback()
			raise UnexpectedError(str(e))

	@staticmethod
	async def _validate_parent_id(data, pk: ID):
		if data.parent_id is None:
			pass

		elif data.parent_id == pk:
			raise CategoryUnprocessableEntity(pk, data.parent_id)

	async def create(self, data):
		await self._validate_parent_id(data, data.id)
		return await self._execute_with_error_handling(self._create, data)

	async def _create(self, data) -> Model:
		"""Creating new entry in table"""
		# Creating variable with new entry data
		instance = self.model(**data.model_dump())
		# Creating new entry
		self.session.add(instance)
		# Commit the changes to the database
		await self.session.commit()
		# Update the object to reflect the new values
		await self.session.refresh(instance)

		return instance

	async def get_by_id(self, pk: ID) -> Model | None:
		"""Get the object by Primary Key (PK)"""
		try:
			# Creating variable with the resulting entry
			obj = await self.session.get(self.model, pk)
			# Check if the object exists
			if obj is None:
				raise CategoryNotFounded(pk)
			return obj

		except CategoryNotFounded as e:
			raise e

		except Exception as e:
			raise UnexpectedError(str(e))

	async def put(self, pk: int, data):
		await self._validate_parent_id(data, data.parent_id)
		return await self._execute_with_error_handling(self._put, pk, data)

	async def _put(self, pk: ID, data: BaseModel) -> Model | None:
		"""Replace the entire record with new data"""
		# Check if the object exists
		obj = await self.session.get(self.model, pk)

		if not obj:
			raise CategoryNotFounded(pk)
		if obj:
			# Replacing entire record
			for key, value in data.model_dump().items():
				setattr(obj, key, value)
			# Commit the changes to the database
			await self.session.commit()
			# Update the object to reflect the updated values
			await self.session.refresh(obj)

		return obj

	# async def patch(self, pk: int, data):
	# 	await self._validate_parent_id(data, data.primary_key)
	# 	return await self._execute_with_error_handling(self._patch, pk, data)
	#
	# async def _patch(self, pk: ID, data: BaseModel) -> Model | None:
	# 	"""Update a record by Primary Key (PK)"""
	# 	# Check if the object exists
	# 	obj = await self.session.get(self.model, pk)
	# 	if not obj:
	# 		raise CategoryNotFounded()
	# 	if obj:
	# 		# Unpack the Pydantic model into a dictionary
	# 		update_data = data.model_dump(exclude_unset=True)  # Only update fields that were provided
	# 		# Update the objects attributes
	# 		for key, value in update_data.items():
	# 			setattr(obj, key, value)
	# 		# Commit the changes to the database
	# 		await self.session.commit()
	# 		# Update the object to reflect the updated values
	# 		await self.session.refresh(obj)
	#
	# 	return obj

	async def delete_by_id(self, pk: int):
		return await self._execute_with_error_handling(self._delete_by_id, pk)

	async def _delete_by_id(self, pk: ID) -> None:
		"""Delete a record by Primary Key (PK)"""
		# Creating query with data for delete
		query = delete(self.model).where(pk == self.model.id)
		# Executing query for delete
		result = await self.session.execute(query)
		# Check if the object exists
		if result.rowcount == 0:
			raise CategoryNotFounded(pk)
		# Commit the changes to the database
		await self.session.commit()

	async def filter(self, *expressions: BinaryExpression) -> list[Model]:
		"""Filtering with where"""
		query = select(self.model)
		if expressions:
			query = query.where(*expressions)
		result = await self.session.scalars(query)

		return list(result)
