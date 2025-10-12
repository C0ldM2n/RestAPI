from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_session
from core.dependencies.providers import create_get_entity_by_id_dependency
from products.products.models import Product
from products.products.repository import ProductRepository


# Product repository dependency
def get_product_repository(
    session: AsyncSession = Depends(get_session),
) -> ProductRepository:
    """Dependency provider for ProductRepository."""
    return ProductRepository(session=session)


ProductRepositoryDep = Annotated[ProductRepository, Depends(get_product_repository)]

# Get product by id dependency
get_product_by_id = create_get_entity_by_id_dependency(get_product_repository)

ProductFromPath = Annotated[Product, Depends(get_product_by_id)]
