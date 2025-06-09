from typing import Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import BaseModel, TreeMixin, TimestampMixin, UserMixin

if TYPE_CHECKING:
    from products.products.models import Product


class Category(BaseModel, TreeMixin, TimestampMixin, UserMixin):
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
    __table_args__ = (
        CheckConstraint(
            "id != parent_id",
            name="ck_categories_id_parent_id_not_self"
        ),
        UniqueConstraint(
            "name", "parent_id",
            name="uq_categories_name_level"
        ),
        UniqueConstraint(
            "sort_order", "parent_id",
            name="uq_categories_sort_order_level"
        ),
    )
