from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Path

from core.db.repository import ID, Model
from core.db.repository.interfaces import IRepository
from core.exceptions.base import NotFoundError


def create_get_entity_by_id_dependency(
    repo_provider: Callable[..., IRepository[Model, ID]],
) -> Callable[[ID, IRepository[Model, ID]], Model]:
    """
    A factory that creates a universal dependency for retrieving
    an entity by ID from a path.

    Args:
        repo_provider: A provider function for a specific repository
        (e.g., get_category_repository).

    Returns:
        An asynchronous dependency function ready for use in FastAPI.
    """

    async def _get_entity_by_id(
        id: Annotated[int, Path(description="Unique entity identifier", gt=0)],
        repo: IRepository[Model, ID] = Depends(repo_provider),
    ) -> Model:
        """
        A universal dependency that extracts entity from a database.
        """
        entity = await repo.read(pk=id)

        if entity is None:
            # We use the ENTITY_NAME constant from the repository class
            entity_name = getattr(repo.__class__, "ENTITY_NAME", "Entity")
            raise NotFoundError(entity_name=entity_name, pk=id)

        return entity

    return _get_entity_by_id
