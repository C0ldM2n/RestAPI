from abc import ABC, ABCMeta, abstractmethod
from typing import Generic

from pydantic import BaseModel

from core.db.repository import ID, Model


class ICreate(ABC, Generic[Model]):
    @abstractmethod
    async def create(self, data: BaseModel) -> Model: ...


class IRead(ABC, Generic[Model, ID]):
    @abstractmethod
    async def read(self, pk: ID) -> Model: ...


class IUpdate(ABC, Generic[Model, ID]):
    @abstractmethod
    async def update(self, pk: ID, data: BaseModel) -> Model: ...


class IDelete(ABC, Generic[ID]):
    @abstractmethod
    async def delete(self, pk: ID) -> None: ...


class IRepository(
    ICreate[Model],
    IRead[Model, ID],
    IUpdate[Model, ID],
    IDelete[ID],
    Generic[Model, ID],
    metaclass=ABCMeta,
):
    """Full CRUD-interface."""

    ...
