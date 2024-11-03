import typing

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from core.db import Base, TreeMixin, TimeMixin, UserMixin

if typing.TYPE_CHECKING:
	from products.products.models import Product


class Category(Base, TreeMixin, TimeMixin, UserMixin):
	__table_args__ = (
		# UniqueConstraint("id", "parent_id", name="uq_id_parent_id"),
		UniqueConstraint("name", "parent_id", name="uq_name_parent_id"),
	)

	__tablename__ = "categories"

	# id: Mapped[int] = mapped_column(primary_key=True, index=True)
	# parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)
	image_url: Mapped[str] = mapped_column(nullable=True)
	name: Mapped[str] = mapped_column(nullable=False)
	is_active: Mapped[bool] = mapped_column(default=False)

	products: Mapped[list["Product"]] = relationship(back_populates="category")

	@validates("parent_id")
	def validate_parent_id(self, key, parent_id):
		if parent_id == self.id:
			raise ValueError("A category cannot be its own parent.")
		return parent_id
