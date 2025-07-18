import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from core.exceptions.base import BaseError
from core.exceptions.responses import ErrorResponse, ErrorResponseMulti


class ErrorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except BaseError as err:
            payload = ErrorResponseMulti(
                errors=[ErrorResponse(message=err.message, detail=err.detail)]
            ).model_dump(by_alias=True)
            return JSONResponse(payload, status_code=err.status_code)

        except RequestValidationError as err:
            errs = [
                ErrorResponse(message=e["msg"], path=list(e["loc"]))
                for e in err.errors()
            ]
            payload = ErrorResponseMulti(errors=errs).model_dump(by_alias=True)
            return JSONResponse(
                payload, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        except Exception:
            # traceback.print_exc()
            generic = ErrorResponseMulti(
                errors=[ErrorResponse(message="Internal Server Error")]
            ).model_dump(by_alias=True)
            return JSONResponse(
                generic, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
