import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import BaseModel, TimestampMixin

if typing.TYPE_CHECKING:
    from products.brands.models import Brand


class Country(BaseModel, TimestampMixin):
    __tablename__ = "countries"

    # Define country columns
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, nullable=False
    )

    name: Mapped[str]

    # Relationship for products table
    brands: Mapped[list["Brand"]] = relationship(back_populates="country")

    # Unique constraints for table
