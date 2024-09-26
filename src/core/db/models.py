from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __allow_unmapped__ = True

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
