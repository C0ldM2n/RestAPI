import uuid
from typing import Generic, TypeVar, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, delete, BinaryExpression
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ValidationError

"""Type variables for BaseRepository"""
Model = TypeVar("Model")
# Flexible ID type (int and uuid)
ID = TypeVar("ID", bound=Union[uuid.UUID, int])

"""Custom exceptions"""
class IntegrityConflictException(Exception):
	pass

class NotFoundException(Exception):
	pass


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
			await self.session.rollback()
			raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")
			# raise ValidationError("Integrity constraint violated") from e
		except Exception:
			# Generic error handling
			await self.session.rollback()
			raise HTTPException(status_code=500, detail="An unexpected error occurred")

	async def _validate_parent_id(self, data, pk: ID):
		if data.parent_id == pk:
			raise HTTPException(status_code=409, detail="A category cannot have itself as its parent")

	async def create(self, data):
		await self._validate_parent_id(data, data.parent_id)
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
		# Closing session
		await self.session.close()

		return instance

	async def get_by_id(self, pk: ID) -> Model | None:
		"""Get the object by Primary Key (PK)"""
		try:
			# Creating variable with the resulting entry
			obj = await self.session.get(self.model, pk)
			# Check if the object exists
			if not obj:
				raise HTTPException(status_code=404, detail="Item not found")
			# Closing session
			await self.session.close()

			return obj

		except Exception as e:
			raise e

	async def put(self, pk: int, data):
		await self._validate_parent_id(data, data.parent_id)
		return await self._execute_with_error_handling(self._put, pk, data)

	async def _put(self, pk: ID, data: BaseModel) -> Model | None:
		"""Replace the entire record with new data"""
		# Check if the object exists
		obj = await self.session.get(self.model, pk)

		if not obj:
			raise HTTPException(status_code=404, detail="Item not found")
			# raise IntegrityError(f"{self.model.__name__} with id {pk} not found.")
		if obj:
			# Replacing entire record
			for key, value in data.model_dump().items():
				setattr(obj, key, value)
			# Commit the changes to the database
			await self.session.commit()
			# Update the object to reflect the updated values
			await self.session.refresh(obj)
			# Closing session
			await self.session.close()

		return obj

	async def patch(self, pk: int, data):
		await self._validate_parent_id(data, data.primary_key)
		return await self._execute_with_error_handling(self._patch, pk, data)

	async def _patch(self, pk: ID, data: BaseModel) -> Model | None:
		"""Update a record by Primary Key (PK)"""
		# Check if the object exists
		obj = await self.session.get(self.model, pk)
		if not obj:
			raise HTTPException(status_code=404, detail="Item not found")
		if obj:
			# Unpack the Pydantic model into a dictionary
			update_data = data.model_dump(exclude_unset=True)  # Only update fields that were provided
			# Update the objects attributes
			for key, value in update_data.items():
				setattr(obj, key, value)
			# Commit the changes to the database
			await self.session.commit()
			# Update the object to reflect the updated values
			await self.session.refresh(obj)
			# Closing session
			await self.session.close()

		return obj

	async def delete_by_id(self, pk: int):
		await self._validate_parent_id(data, data.primary_key)
		return await self._execute_with_error_handling(self._delete_by_id, pk)

	async def _delete_by_id(self, pk: ID) -> None:
		"""Delete a record by Primary Key (PK)"""
		# Creating query with data for delete
		query = delete(self.model).where(self.model.id == pk)
		# Executing query for delete
		result = await self.session.execute(query)
		# Check if the object exists
		if result.rowcount == 0:
			raise NotFoundException(f"Record with ID {pk} not found.")
		# Commit the changes to the database
		await self.session.commit()
		# Closing session
		await self.session.close()

		# obj = await self.session.get(self.model, pk)
		# if not obj:
		# 	raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
		#
		# await self.session.delete(obj)
		# await self.session.commit()
		# return {"message": f"{self.model.__name__} deleted successfully"}

	async def filter(self, *expressions: BinaryExpression) -> list[Model]:
		"""Filtering with where"""
		query = select(self.model)
		if expressions:
			query = query.where(*expressions)
		result = await self.session.scalars(query)

		return list(result)

		# except IntegrityError as e:
		#     await self.session.rollback()
		#     raise IntegrityConflictException(f"Could not delete record: {str(e)}")
		#
		# except Exception as e:
		# 	await self.session.rollback()
		# 	raise e
