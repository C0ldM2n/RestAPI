from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    DatabaseError,
    ValidationError,
    AlreadyExistOnThisLevelError,
    NotFoundError,
)

from asyncpg import UniqueViolationError


def handling_repository_errors(func):
    """Decorator for handling repository errors."""

    async def wrapper(self, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            if result is None:
                raise NotFoundError(pk=args[0])
            return result

        except IntegrityError as e:
            # Database integrity error handling
            await self.session.rollback()
            print(e)

            if f"duplicate key value" in str(e.args[0]):
                if f"name_level" in str(e.args[0]):
                    raise AlreadyExistOnThisLevelError(
                        field="name",
                        data=args[0]["name"],
                        detail=str(e.args[0]),
                    )
                elif f"sort_order_level" in str(e.args[0]):
                    raise AlreadyExistOnThisLevelError(
                        field="sort_order",
                        data=args[0]["sort_order"],
                        detail=str(e.args[0]),
                    )
            else:
                raise DatabaseError(detail=str(e.args[0]))

        except ValueError as e:
            # Validating values error handling
            print(10 * "---ValueError---")
            print(e)
            raise DatabaseError(detail=str(e.args[0]))

        except Exception as e:
            # Generic error handling
            await self.session.rollback()
            print(10 * "---Exception---")
            print(e)
            if "not found" in str(e.args[0]):
                # print(args)
                # print(kwargs)
                raise NotFoundError(pk=args[0], detail=str(e.args[0]))

            else:
                raise DatabaseError(detail=str(e.args[0]))

    return wrapper
