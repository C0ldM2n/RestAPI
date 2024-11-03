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

# Old version

# class CategoryCreateSchema(BaseModel):
#     id: Optional[int]
#     parent_id: Optional[int]
#     image_url: Optional[str]
#     name: str
#     is_active: bool
#
#     model_config = ConfigDict(
#         from_attributes = True)
#
# class CategoryReadSchema(BaseModel):
#     id: Optional[int]
#     parent_id: Optional[int]
#     image_url: Optional[str]
#     name: str
#     is_active: bool
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]
#
#     model_config = ConfigDict(
#         from_attributes=True)
#
# class CategoryPutSchema(BaseModel):
#     id: int
#     parent_id: int
#     image_url: str
#     name: str
#     is_active: bool
#
#     model_config = ConfigDict(
#         from_attributes=True)
#
# class CategoryPatchSchema(BaseModel):
#     id: Optional[int]
#     parent_id: Optional[int]
#     image_url: Optional[str]
#     name: Optional[str]
#     is_active: Optional[bool]
#
#     model_config = ConfigDict(
#         from_attributes=True)
