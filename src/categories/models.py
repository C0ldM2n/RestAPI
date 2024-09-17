from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, DateTimeMixin


class Category(Base, DateTimeMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # parent_id: Mapped[int | None] = mapped_column()
    image_url: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(Boolean)
    created_by: Mapped[str] = mapped_column(String)
    updated_by: Mapped[str] = mapped_column(String)

    products: Mapped[list['Product']] = relationship(cascade='all, delete-orphan')

    # products: Mapped[list["Product"]] = relationship(back_populates="category")

    # parent: Mapped["Category"] = relationship("Category", remote_side=[id], backref="subcategories")
