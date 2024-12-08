from uuid import UUID

from starlette.status import HTTP_400_BAD_REQUEST


class BaseError(Exception):
    """Base class for custom errors."""
    def __init__(self, message: str, status_code: int = HTTP_400_BAD_REQUEST, detail: str = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail


class NotFoundError(BaseError):
    def __init__(self, pk: int | UUID, detail: str = None):
        super().__init__(
            f"Entity with id={pk} not found.",
            status_code=404,
            detail = detail or {}
        )


class AlreadyExistError(BaseError):
    def __init__(self, name: str, detail: str = None):
        super().__init__(
            f"Entity with name={name} on this level already exist.",
            status_code=409,
            detail = detail or {}
        )


class UnprocessableEntityError(BaseError):
    def __init__(self, detail: str = None):
        super().__init__(
            f"Entity can't be it's own parent.",
            status_code=422,
            detail=detail or {}
        )


class CyclicReferenceError(BaseError):
    def __init__(self, detail: str = None):
        super().__init__(
            f"Entity can't be it's own child.",
            status_code=422,
            detail=detail or {}
        )

class UnexpectedError(BaseError):
    def __init__(self, detail: str = None):
        super().__init__(
            message=f"An unexpected error occurred.",
            status_code=500,
            detail=detail or {}
        )
