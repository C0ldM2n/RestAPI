from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_session
from core.dependencies.providers import create_get_entity_by_id_dependency
from products.brands.models import Brand
from products.brands.repository import BrandRepository


# Brand repository dependency
def get_brand_repository(
    session: AsyncSession = Depends(get_session),
) -> BrandRepository:
    """Dependency provider for BrandRepository."""
    return BrandRepository(session=session)


BrandRepositoryDep = Annotated[BrandRepository, Depends(get_brand_repository)]

# Get brand by id dependency
get_brand_by_id = create_get_entity_by_id_dependency(get_brand_repository)

BrandFromPath = Annotated[Brand, Depends(get_brand_by_id)]
