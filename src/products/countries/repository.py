from core.db.repository.base_repository import BaseRepository
from products.countries.models import Country


class CountryRepository(BaseRepository[Country, int]):
    """Responsible for country-specific logic."""

    ENTITY_NAME = "Country"

    pass
