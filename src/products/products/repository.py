from uuid import UUID

from core.db.repository.base_repository import BaseRepository
from products.products.models import Product


class ProductRepository(BaseRepository[Product, UUID]):
    """Responsible for product-specific logic."""

    ENTITY_NAME = "Product"

    pass
