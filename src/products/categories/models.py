import typing

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, TreeMixin, TimeMixin, UserMixin

if typing.TYPE_CHECKING:
	from products.products.models import Product


class Category(Base, TimeMixin, UserMixin):

	__tablename__ = "categories"

	# Define category columns
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
	image_url: Mapped[str | None] = mapped_column(nullable=True)
	name: Mapped[str] = mapped_column(nullable=False)
	is_active: Mapped[bool] = mapped_column(default=False)
	# sort_order: Mapped[int] = mapped_column(default=0)

	# Relationship for products table
	products: Mapped[list["Product"]] = relationship(
		"Product",
		back_populates="category"
	)

	# Unique constraints for table
	__table_args__ = (
		UniqueConstraint("name", "parent_id", name="uq_name_per_level"),
	)
