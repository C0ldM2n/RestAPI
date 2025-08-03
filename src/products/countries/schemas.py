from pydantic import BaseModel, ConfigDict


class CountryBaseSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class CountryResponseSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CountryCreateSchema(CountryBaseSchema):
    pass


class CountryUpdateSchema(CountryBaseSchema):
    pass
