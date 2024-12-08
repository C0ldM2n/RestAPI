from .base import BaseError


class ValidationError(BaseError):
    def __init__(self, detail: str = None):
        super().__init__(
            f"Validation error in the request body.",
            status_code=422,
            detail=detail or {}
        )


class ValidationQueryError(BaseError):
    def __init__(self, detail: str = None):
        super().__init__(
            f"Entity can't be it's own child.",
            status_code=422,
            detail=detail or {}
        )


class BadRequestError(BaseError):
    def __init__(self, detail: str = None):
        super().__init__(
            f"Bad request error.",
            status_code=400,
            detail=detail or {}
        )


class DatabaseIntegrityError(BaseError):
    def __init__(self, detail: str = None):
        super().__init__(
            f"Database integrity error.",
            status_code=400,
            detail=detail or {}
        )


# Example
# class ValidationError(RequestValidationError):
#     def __init__(self, details: list):
#         super().__init__([
#             {
#                 "loc": err["loc"],
#                 "msg": err["msg"],
#                 "type": "value_error"
#             }
#             for err in details
#         ])
#
#
# class ValidationQueryError(RequestValidationError):
#     def __init__(self, query_param: str, reason: str):
#         super().__init__([
#             {
#                 "loc": ["query", query_param],
#                 "msg": reason,
#                 "type": "value_error.query"
#             }
#         ])
