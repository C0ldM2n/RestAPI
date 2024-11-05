from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, validates


class TreeMixin(object):
	"""A mixin class to represent hierarchical relationships in a tree structure."""

	__tablename__: str

	@declared_attr
	def id(cls) -> Mapped[int]:
		return mapped_column(primary_key=True, autoincrement=True)

	@declared_attr
	def parent_id(cls) -> Mapped[int | None]:
		return mapped_column(ForeignKey(f"{cls.__tablename__}.id"), nullable=True)

	# __table_args__ = (UniqueConstraint("name", "parent_id", name="uq_name_per_level"),)

	@declared_attr
	def __table_args__(cls):
		return (UniqueConstraint("name", "parent_id", name="uq_name_per_level"),)

	@validates("parent_id")
	def validate_parent_id(self, key, parent_id):
		"""Ensure parent_id does not reference itself as its own parent."""
		if parent_id == self.id:
			raise ValueError("A node cannot be its own parent.")
		return parent_id


	# async def is_descendant_of(self, session: AsyncSession, ancestor_id: int) -> bool:
	# 	"""Check if the current instance is a descendant of a given ancestor ID."""
	# 	current = self
	# 	while current.parent_id is not None:
	# 		if current.parent_id == ancestor_id:
	# 			return True
	# 		result = await session.execute(select(Category).filter_by(id=current.parent_id))
	# 		current = result.scalar_one_or_none()
	# 		if current is None:
	# 			break
	# 	return False
