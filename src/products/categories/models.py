from typing import Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from core.db import Base, TreeMixin, SortMixin, TimeMixin, UserMixin

if TYPE_CHECKING:
    from products.products.models import Product


class Category(Base, TreeMixin, TimeMixin, UserMixin):
    __tablename__ = "categories"

    # Define category columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)

    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationship for products table
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="categories"
    )

    # parent: Mapped[Optional["Category"]]= relationship(
    #     "Category", remote_side="Category.id", backref=backref("children", cascade="all"),
    # )

    # Unique constraints for table
    __table_args__ = (
        UniqueConstraint("name", "parent_id", name="uq_categories_name_level"),
        UniqueConstraint(
            "sort_order", "parent_id", name="uq_categories_sort_order_level"
        ),
    )
