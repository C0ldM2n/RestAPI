from pydantic import BaseModel, ConfigDict

class BrandCreate(BaseModel):
    country_registration_id: int
    name: str

    model_config = ConfigDict(
        from_attributes = True)
