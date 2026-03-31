from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_session
from core.dependencies.providers import create_get_entity_by_id_dependency
from products.categories.models import Category
from products.categories.repository import CategoryRepository


# Category repository dependency
def get_category_repository(
    session: AsyncSession = Depends(get_session),
) -> CategoryRepository:
    """Dependency provider for CategoryRepository."""
    return CategoryRepository(session=session)


CategoryRepositoryDep = Annotated[CategoryRepository, Depends(get_category_repository)]

# Get category by id dependency
get_category_by_id = create_get_entity_by_id_dependency(get_category_repository)

CategoryFromPath = Annotated[Category, Depends(get_category_by_id)]
