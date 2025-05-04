from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryBaseSchema(BaseModel):
    parent_id: Optional[int] = None
    image_url: Optional[str] = None
    name: str
    is_active: bool
    sort_order: int = 1

    model_config = ConfigDict(from_attributes=True)


class CategoryResponseSchema(BaseModel):
    id: int
    parent_id: Optional[int]
    image_url: Optional[str]
    name: str
    is_active: bool
    sort_order: int
    lft: int
    rgt: int
    level: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryCreateSchema(CategoryBaseSchema):
    pass


class CategoryUpdateSchema(CategoryBaseSchema):
    pass
