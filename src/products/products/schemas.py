from pydantic import UUID4, BaseModel, ConfigDict


class ProductBaseSchema(BaseModel):
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


class ProductResponseSchema(BaseModel):
    id: UUID4
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


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductUpdateSchema(ProductBaseSchema):
    pass
