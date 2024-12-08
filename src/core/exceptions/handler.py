from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY

from .base import BaseError
from .response import create_error_response

def setup_exception_handlers(app):
    """Setup exception handlers."""
    app.add_exception_handler(BaseError, base_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

async def base_error_handler(_: Request, error: BaseError) -> JSONResponse:
    """Handler for base errors."""
    return create_error_response(
        message=error.message,
        status=error.status_code,
        detail=error.detail,
    )

async def validation_error_handler(_: Request, error: RequestValidationError) -> JSONResponse:
    """Handler for validation errors."""
    details = [{"message": err["msg"], "path": list(err["loc"])} for err in error.errors()]
    return create_error_response(
        message="Validation error",
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        detail=details,
    )

async def unhandled_exception_handler(_: Request, error: Exception) -> JSONResponse:
    """Handler for unhandled exceptions."""
    return create_error_response(
        message="Unhandled error occurred",
        status=HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(error),
    )
