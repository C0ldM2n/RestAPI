from pydantic import BaseModel, ConfigDict, UUID4


class ProductCreate(BaseModel):
    name: str
    brand_id: int
    category_id: int
    price: int
    sku: str | None
    isbn: str | None
    quantity: int
    published: bool
    created_by: UUID4 | None
    updated_by: UUID4 | None

    model_config = ConfigDict(from_attributes=True)
