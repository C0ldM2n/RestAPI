import typing
import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import BaseModel, TimeMixin

if typing.TYPE_CHECKING:
    from products.brands.models import Brand


class User(BaseModel, TimeMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)

    # TODO: create password and email mixin

    # brands: Mapped[list["Brand"]] = relationship(back_populates="user")
