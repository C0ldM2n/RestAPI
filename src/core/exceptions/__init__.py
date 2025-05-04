from .base import (
    NotFoundError,
    AlreadyExistOnThisLevelError,
    UnprocessableEntityError,
    CyclicReferenceError,
)

from .validation import (
    ValidationError,
    ValidationQueryError,
    BadRequestError,
    DatabaseError,
)

ValidationExceptions = [
    "ValidationError",
    "ValidationQueryError",
    "DatabaseIntegrityError",
]

BaseExceptions = [
    "NotFoundError",
    "AlreadyExistError",
    "UnprocessableEntityError",
    "CyclicReferenceError",
]

__all__ = [
    "NotFoundError",
    "AlreadyExistOnThisLevelError",
    "UnprocessableEntityError",
    "CyclicReferenceError",
    "ValidationError",
    "ValidationQueryError",
    "BadRequestError",
    "DatabaseError",
]
