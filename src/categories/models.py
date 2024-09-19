import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, DateTimeMixin

if typing.TYPE_CHECKING:
    from products.models import Product


class Category(Base, DateTimeMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    parent_id: Mapped[int | None] = mapped_column(nullable=True)
    image_url: Mapped[str]
    active: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[str] = mapped_column(nullable=True)
    updated_by: Mapped[str] = mapped_column(nullable=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")
