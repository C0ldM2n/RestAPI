from pydantic import BaseModel, ConfigDict


class BrandBaseSchema(BaseModel):
    country_registration_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class BrandResponseSchema(BaseModel):
    id: int
    country_registration_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class BrandCreateSchema(BrandBaseSchema):
    pass


class BrandUpdateSchema(BrandBaseSchema):
    pass
