from typing import Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, HierarchicalMixin, TimeMixin, UserMixin

if TYPE_CHECKING:
    from products.products.models import Product


class Category(Base, HierarchicalMixin, TimeMixin, UserMixin):
    __tablename__ = "categories"

    # Define category columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationship for products table
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="categories"
    )

    # Unique constraints for table
    # __table_args__ = (
    #
    # )
