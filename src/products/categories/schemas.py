from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class CategoryBaseSchema(BaseModel):
    parent_id: Optional[int]
    image_url: Optional[str]
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True)

class CategoryResponseSchema(CategoryBaseSchema):
    id: Optional[int]
    created_at: datetime
    updated_at: datetime

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryUpdateSchema(CategoryBaseSchema):
    pass
