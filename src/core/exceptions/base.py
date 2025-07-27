from typing import Any
from uuid import UUID

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class BaseError(Exception):
    """Base class for custom errors."""

    def __init__(
        self,
        *_: tuple[Any],
        message: str,
        status_code: int = HTTP_400_BAD_REQUEST,
        detail: dict = None,
    ) -> None:
        self.message: str = message
        self.status_code: int = status_code
        self.detail: dict | str | None = detail

        super().__init__(message)


class NotFoundError(BaseError):
    def __init__(self, *_: tuple[Any], pk: int | UUID) -> None:
        super().__init__(
            message=f"Entity with id {pk} not found.",
            status_code=HTTP_404_NOT_FOUND,
            detail="Result = None. Entity not found.",
        )


class AlreadyExistOnThisLevelError(BaseError):
    def __init__(
        self, *_: tuple[Any], field: str, data: str | int, detail: str = None
    ) -> None:
        super().__init__(
            message=(
                f"Entity with {field} '{data}' on this level already exists."
            ),
            status_code=HTTP_409_CONFLICT,
            detail=detail or {},
        )


class ForeignKeyConstraintViolationError(BaseError):
    def __init__(
        self, *_: tuple[Any], field: str, data: str | int, detail: str = None
    ) -> None:
        super().__init__(
            message=f"Foreign key {field} '{data}' not found.",
            status_code=HTTP_409_CONFLICT,
            detail=detail or {},
        )


class SelfParentError(BaseError):
    def __init__(self, *_: tuple[Any]) -> None:
        super().__init__(
            message="Entity can't be it's own parent.",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parent ID cannot be the same as the entity's ID.",
        )


class CyclicReferenceError(BaseError):
    def __init__(self, *_: tuple[Any]) -> None:
        super().__init__(
            message="Entity can't be it's own child.",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Entity cannot be assigned as a parent to itself, "
                "either directly or through a chain of relationships."
            ),
        )


class DatabaseError(BaseError):
    def __init__(self, *_: tuple[Any], detail: str = None) -> None:
        super().__init__(
            message="Database error.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail or {},
        )
