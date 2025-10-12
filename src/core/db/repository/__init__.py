from typing import TypeVar, Union
from uuid import UUID

Model = TypeVar("Model")
ID = TypeVar("ID", bound=int | UUID)
