import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import BaseModel

if typing.TYPE_CHECKING:
    from products.products.models import Product
    from products.countries.models import Country


class Brand(BaseModel):
    __tablename__ = "brands"

    # Define brand columns
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, nullable=False
    )

    country_registration_id: Mapped[int | None] = mapped_column(
        ForeignKey("countries.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship for products table
    products: Mapped[list["Product"]] = relationship(back_populates="brands")
    country: Mapped["Country"] = relationship(back_populates="brands")

    # Unique constraints for table
