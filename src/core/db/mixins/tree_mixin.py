from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, validates, relationship


class TreeMixin:
	"""A mixin class to represent hierarchical relationships in a tree structure."""

	__tablename__: str

	@declared_attr
	def rgt(cls) -> Mapped[int]:
		return mapped_column(nullable=False)

	@declared_attr
	def lft(cls) -> Mapped[int]:
		return mapped_column(nullable=False)

	@declared_attr
	def level(cls) -> Mapped[int]:
		return mapped_column(nullable=False)

	@declared_attr
	def parent_id(cls) -> Mapped[int | None]:
		return mapped_column(ForeignKey(f"{cls.__tablename__}.id"), nullable=True)

	@declared_attr
	def parent(cls):
		# Mapped[list[cls.__tablename__]] =
		relationship(
			cls.__tablename__,
			back_populates="children",
			remote_sidef="{cls.__tablename__}.id",
		)

	@declared_attr
	def children(cls):
		relationship(
			cls.__tablename__,
			back_populates="parent",
			cascade="all, delete-orphan",
			single_parent=True
		)

	@declared_attr
	def __table_args__(cls):
		return *cls.__table_args__ + UniqueConstraint("name", "parent_id", name="uq_name_per_level"),

	@validates("parent_id")
	def validate_parent_id(self, key, parent_id):
		"""Ensure parent_id does not reference itself as its own parent."""
		# if parent_id == self.id:
		if parent_id is not None and parent_id == f"{self.__tablename__}.id":
			raise ValueError("A node cannot be its ownparent.")
		return parent_id
