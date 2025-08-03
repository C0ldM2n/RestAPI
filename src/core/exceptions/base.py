from typing import Any
from uuid import UUID

from starlette import status

from core.exceptions.schemas import ErrorCode


class BaseError(Exception):
    """Base class for all custom API errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: ErrorCode = ErrorCode.UNEXPECTED_ERROR
    message: str = "An error has occurred."
    path: list[str | int] | None = None

    def __init__(
        self,
        message: str | None = None,
        path: list[str | int] | None = None,
    ):
        if message:
            self.message = message
        if path:
            self.path = path
        super().__init__(self.message)


class NotFoundError(BaseError):
    status_code = status.HTTP_404_NOT_FOUND
    code = ErrorCode.ENTITY_NOT_FOUND

    def __init__(self, entity_name: str, pk: int | UUID):
        super().__init__(
            message=f"Entity '{entity_name}' with ID '{pk}' not found."
        )


class AlreadyExistsError(BaseError):
    status_code = status.HTTP_409_CONFLICT
    code = ErrorCode.ENTITY_ALREADY_EXISTS

    def __init__(self, entity_name: str, field: str, value: Any):
        super().__init__(
            message=f"Entity '{entity_name}' with field '{field}' = '{value}' already exists.",
            path=[field],
        )


class ForeignKeyViolationError(BaseError):
    status_code = status.HTTP_409_CONFLICT
    code = ErrorCode.FOREIGN_KEY_VIOLATION

    def __init__(self, entity_name: str, field: str, value: Any):
        super().__init__(
            message=f"Unable to create/update '{entity_name}': related entity with '{field}' = '{value}' not found.",
            path=[field],
        )


class SelfParentError(BaseError):
    """Error when an entity assigns itself as its parent."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = ErrorCode.SELF_PARENT_ERROR
    message = "Entity cannot be its own parent."

    def __init__(self):
        super().__init__(path=["parent_id"])


class CyclicReferenceError(BaseError):
    """Error when a cycle is detected in the hierarchy."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = ErrorCode.CYCLIC_DEPENDENCY_ERROR
    message = "Cyclical dependency has been detected: you cannot make a parent a child element."

    def __init__(self):
        super().__init__(path=["parent_id"])


class DatabaseError(BaseError):
    """General error for unexpected database failures that could not be recognized."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = ErrorCode.DATABASE_ERROR
    message = "An unexpected database error has occurred."

    def __init__(self):
        super().__init__()
