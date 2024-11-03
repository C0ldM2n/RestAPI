from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class TreeMixin:
	__table_args__ = (
		UniqueConstraint("id", "parent_id", name="uq_id_parent_id")
	)

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)
