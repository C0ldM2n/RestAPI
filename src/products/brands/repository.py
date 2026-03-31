from core.db.repository.base_repository import BaseRepository
from products.brands.models import Brand


class BrandRepository(BaseRepository[Brand, int]):
    """Responsible for brand-specific logic."""

    ENTITY_NAME = "Brand"

    pass
