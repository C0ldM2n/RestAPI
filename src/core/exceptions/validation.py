from typing import Any

from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from core.exceptions.base import BaseError


class ValidationError(BaseError):
    def __init__(self, *_: tuple[Any], detail: str = None) -> None:
        super().__init__(
            message=f"Validation error in the request body.",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail or {},
        )


class ValidationQueryError(BaseError):
    def __init__(self, *_: tuple[Any], detail: str = None) -> None:
        super().__init__(
            message=f"Entity can't be it's own child.",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail or {},
        )


class BadRequestError(BaseError):
    def __init__(self, *_: tuple[Any], detail: str = None) -> None:
        super().__init__(
            message=f"Bad request error.",
            status_code=HTTP_400_BAD_REQUEST,
            detail=detail or {},
        )


class DatabaseError(BaseError):
    def __init__(self, *_: tuple[Any], detail: str = None) -> None:
        super().__init__(
            message=f"Database error.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail or {},
        )
