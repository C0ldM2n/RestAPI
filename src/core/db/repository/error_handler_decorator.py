import traceback
from functools import wraps
from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    DatabaseError,
    AlreadyExistOnThisLevelError,
    NotFoundError,
    UnprocessableEntityError, CyclicReferenceError, ForeignKeyConstraintViolationError,
)


def handling_repository_errors(
        *,
        handle_integrity: bool = True,
        handle_validation: bool = True,
        handle_not_found: bool = True,
):
    """
    Декоратор‑фабрика: по флагам решает, какие ошибки ловить.
    handle_integrity  — IntegrityError → AlreadyExistOnThisLevel/DatabaseError
    handle_validation — ValueError → UnprocessableEntityError
    handle_not_found  — result is None → NotFoundError
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                result = await func(self, *args, **kwargs)

                if handle_not_found and result is None:
                    pk = args[0] if not isinstance(args[0], dict) else args[0]["id"]
                    detail = "Result = None. Entity not found."
                    raise NotFoundError(pk=pk, detail=detail)

                return result

            except IntegrityError as e:
                await self._session.rollback()
                if not handle_integrity:
                    raise

                detail = str(e.orig)
                if "already exists" in detail:
                    field = detail.split("Key (")[1].split(",")[0]
                    data = detail.split("=(")[1].split(",")[0]
                    raise AlreadyExistOnThisLevelError(
                        field=field,
                        data=data,
                        detail=detail,
                    )
                elif "id_not_parent" in detail:
                    raise CyclicReferenceError(detail=detail)
                elif "not present" in detail:
                    field = detail.split("Key (")[1].split(")")[0]
                    data = detail.split("=(")[1].split(")")[0]
                    raise ForeignKeyConstraintViolationError(
                        field=field,
                        data=data,
                        detail=detail
                    )

                raise DatabaseError(detail=detail)

            except ValueError as e:
                detail=str(e)
                await self._session.rollback()
                if not handle_validation:
                    raise
                raise UnprocessableEntityError(detail=detail)

            except Exception as e:
                detail=str(e)
                await self._session.rollback()
                if isinstance(e, NotFoundError):
                    raise
                print(traceback.format_exc())
                raise DatabaseError(detail=detail)

        return wrapper

    return decorator
