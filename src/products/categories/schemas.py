from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CategoryBaseSchema(BaseModel):
    parent_id: int | None = None
    image_url: str | None = None
    name: str
    is_active: bool
    sort_order: int = 1

    model_config = ConfigDict(from_attributes=True)


class CategoryResponseSchema(BaseModel):
    id: int
    parent_id: int | None
    image_url: str | None
    name: str
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryCreateSchema(CategoryBaseSchema):
    pass


class CategoryUpdateSchema(CategoryBaseSchema):
    pass
