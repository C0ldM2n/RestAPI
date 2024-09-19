from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, DateTimeMixin
from brands.models import Brand
from categories.models import Category


class Product(Base, DateTimeMixin):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str]
    price: Mapped[int]
    sku: Mapped[str]
    isbn: Mapped[str]
    quantity: Mapped[int]
    published: Mapped[bool]
    created_by: Mapped[str]
    updated_by: Mapped[str]

    brand: Mapped["Brand"] = relationship(back_populates="products")
    category: Mapped["Category"] = relationship(back_populates="products")
