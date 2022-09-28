from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

from app.schemas.charity_project import SchemaBaseModel


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(SchemaBaseModel):
    id: int
    comment: Optional[str]
    user_id: Optional[int]

    class Config:
        orm_mode = True
