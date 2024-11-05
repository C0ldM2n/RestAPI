import typing

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from core.db import Base, TreeMixin, TimeMixin, UserMixin

if typing.TYPE_CHECKING:
	from products.products.models import Product


class Category(Base, TreeMixin, TimeMixin, UserMixin):
	# Unique constraint for name within the same level of the tree
	# __table_args__ = (
	# 	UniqueConstraint("name", "parent_id", name="uq_category_name_per_level"),
	# )

	__tablename__ = "categories"

	# Define category columns
	image_url: Mapped[str] = mapped_column(nullable=True)
	name: Mapped[str] = mapped_column(nullable=False)
	is_active: Mapped[bool] = mapped_column(default=False)

	# Relationship for children and products
	# children: Mapped[list["Category"]] = relationship("Category", backref="parent", remote_side="Category.id")
	products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

	@validates("parent_id")
	def validate_parent_id(self, key, parent_id):
		"""Ensure a category does not reference itself as its parent."""
		if parent_id == self.id:
			raise ValueError("A category cannot be its own parent.")
		return parent_id
