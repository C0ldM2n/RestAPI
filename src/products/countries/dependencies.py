from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_session
from products.countries.models import Country
from products.countries.repository import CountryRepository
from core.dependencies.providers import create_get_entity_by_id_dependency


# Country repository dependency
def get_country_repository(
    session: AsyncSession = Depends(get_session),
) -> CountryRepository:
    """Dependency provider for CountryRepository."""
    return CountryRepository(session=session)


CountryRepositoryDep = Annotated[
    CountryRepository, Depends(get_country_repository)
]

# Get country by id dependency
get_country_by_id = create_get_entity_by_id_dependency(get_country_repository)

CountryFromPath = Annotated[Country, Depends(get_country_by_id)]
