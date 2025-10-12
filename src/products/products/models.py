import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import BaseModel, TimestampMixin
from products.brands.models import Brand
from products.categories.models import Category


class Product(BaseModel, TimestampMixin):
    __tablename__ = "products"

    # Define product columns
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    name: Mapped[str]
    price: Mapped[int]
    sku: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    isbn: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    quantity: Mapped[int]
    published: Mapped[bool]

    created_by: Mapped[UUID | None] = mapped_column(UUID, nullable=True)
    updated_by: Mapped[UUID | None] = mapped_column(UUID, nullable=True)

    # Relationship for products table
    brands: Mapped["Brand"] = relationship(
        "Brand",
        # secondary=str("brands_products"),
        back_populates="products",
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        # secondary="categories",
        back_populates="products",
    )

    # Unique constraints for table
