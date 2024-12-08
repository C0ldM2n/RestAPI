from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .base import BaseError


class TableError(BaseError):
    """Error class for table operations."""
    def __init__(self, table_name: str, issue: str, detail: dict = None):
        message = f"Issue with table '{table_name}': {issue}"
        super().__init__(message=message, status_code=HTTP_400_BAD_REQUEST, detail=detail)

# ...