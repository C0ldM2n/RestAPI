from sqlalchemy.ext.asyncio import AsyncSession

from core.db.repository import BaseRepository
from models import Brand

class BrandRepository(BaseRepository[Brand, int]):
    """Repository for managing brand-related queries."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Brand, session)
