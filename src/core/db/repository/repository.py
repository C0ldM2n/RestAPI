from uuid import UUID
from typing import Generic, TypeVar, Union

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (
    NotFoundError,
    AlreadyExistOnThisLevelError,
    UnprocessableEntityError,
)
from .handler import handling_repository_errors
from ..tree.utils import validate_no_cycless

Model = TypeVar("Model")
ID = TypeVar("ID", bound=Union[UUID, int])


class BaseRepository(Generic[Model, ID]):
    """Generic repository for performing database queries with flexible ID types."""

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        """Initialize with model and session."""
        self.model = model
        self.session = session

    # @staticmethod
    # async def _validate_parent_id(data, pk: ID):
    #     """Helper method to prevent cycle creation."""
    #     if data.parent_id is None:
    #         pass
    #
    #     elif data.parent_id == pk:
    #         raise UnprocessableEntityError()

    # async def _validate_duplicate(self, data: dict):
    #     """Check if an entity with the same name and parent_id already exists."""
    #     # Creating variable with the resulting entry
    #     existing_entity = await self.session.execute(
    #         select(self.model).filter_by(
    #             name=data["name"], parent_id=data["parent_id"]
    #         )
    #     )
    #     if existing_entity.scalars().first():
    #         raise AlreadyExistOnThisLevelError(field="name", data=data["name"])

    # async def _create(self, data: dict):
    # 	await self._validate_duplicate(data)
    # 	return await self._execute_with_error_handling(self._create, data)

    @handling_repository_errors
    async def create(self, data: dict) -> Model:
        """Creating new entry in table."""

        # Creating variable with new entry data
        instance = self.model(**data)
        # Creating new entry
        self.session.add(instance)
        # Commit the changes to the database
        await self.session.commit()

        return instance

    @handling_repository_errors
    async def get_by_id(self, pk: ID) -> Model | None:
        """Get the object by Primary Key."""
        obj = await self.session.get(self.model, pk)
        return obj

    # async def put(self, pk: int, data: dict):
    # 	await self._validate_duplicate(data)
    # 	return await self._execute_with_error_handling(self._put, pk, data)

    @handling_repository_errors
    async def put(self, pk: ID, data: dict) -> Model | None:
        """Replace the entire record with new data."""
        obj = await self.session.get(self.model, pk)

        if obj:
            print(data["parent_id"])
            await validate_no_cycless(self, pk, data["parent_id"])
            # Replacing entire record
            for key, value in data.items():
                setattr(obj, key, value)
            # Commit the changes to the database
            await self.session.commit()
            # Update the object to reflect the updated values
            await self.session.refresh(obj)

        return obj

    # async def delete_by_id(self, pk: int):
    # 	return await self._execute_with_error_handling(self._delete_by_id, pk)

    # @handling_repository_errors
    async def delete_by_id(self, pk: ID) -> None:
        """Delete a record by Primary Key."""
        # Creating query with data for delete
        query = delete(self.model).where(pk == self.model.id)
        # Executing query for delete
        result = await self.session.execute(query)
        # Check if the object exists
        # if result.rowcount == 0:
        #     raise NotFoundError(pk=pk)
        # Commit the changes to the database
        await self.session.commit()


# async def filter(self, *expressions: BinaryExpression) -> list[Model]:
# 	"""Filtering with where."""
# 	query = select(self.model)
# 	if expressions:
# 		query = query.where(*expressions)
# 	result = await self.session.scalars(query)
#
# 	return list(result)
