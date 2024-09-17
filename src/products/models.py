from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base, DateTimeMixin


class Product(Base, DateTimeMixin):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    sku: Mapped[str] = mapped_column(String)
    isbn: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    published: Mapped[bool] = mapped_column(Boolean)
    created_by: Mapped[str] = mapped_column(String)
    updated_by: Mapped[str] = mapped_column(String)

    brand: Mapped["Brand"] = relationship(back_populates="products")
    category: Mapped["Category"] = relationship(back_populates="products")

    # category: Mapped["Category"] = relationship("Category", back_populates="products")
    # brand: Mapped["Brand"] = relationship("Brand", back_populates="products")

