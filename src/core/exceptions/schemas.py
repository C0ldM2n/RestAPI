from enum import Enum

from pydantic import BaseModel


class ErrorCode(str, Enum):
    """Custom error Enums."""

    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    ENTITY_ALREADY_EXISTS = "ENTITY_ALREADY_EXISTS"
    FOREIGN_KEY_VIOLATION = "FOREIGN_KEY_VIOLATION"
    SELF_PARENT_ERROR = "SELF_PARENT_ERROR"
    CYCLIC_DEPENDENCY_ERROR = "CYCLIC_DEPENDENCY_ERROR"


class ApiError(BaseModel):
    """Error scheme."""

    code: ErrorCode
    message: str
    path: list[str | int] | None = None


class ApiErrorResponse(BaseModel):
    """API error response scheme."""

    errors: list[ApiError]
