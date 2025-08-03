from products.categories.models import Category
from core.db.repository.hierarchical_repository import HierarchicalRepository


class CategoryRepository(HierarchicalRepository[Category, int]):
    """Responsible for category-specific logic."""

    ENTITY_NAME = "Category"

    pass
