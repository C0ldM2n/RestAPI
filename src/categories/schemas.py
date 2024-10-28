from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    id: Optional[int]
    parent_id: Optional[int]
    image_url: Optional[str]
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes = True)

class CategoryRead(BaseModel):
    id: Optional[int]
    parent_id: Optional[int]
    image_url: Optional[str]
    name: str
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True)

class CategoryPut(BaseModel):
    id: int
    parent_id: int
    image_url: str
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True)

class CategoryPatch(BaseModel):
    id: Optional[int]
    parent_id: Optional[int]
    image_url: Optional[str]
    name: Optional[str]
    is_active: Optional[bool]

    model_config = ConfigDict(
        from_attributes=True)
