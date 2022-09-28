from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt


class SchemaBaseModel(BaseModel):
    full_amount: Optional[PositiveInt]
    invested_amount: Optional[NonNegativeInt] = 0
    fully_invested: Optional[bool] = False
    create_date: Optional[datetime]
    close_date: Optional[datetime]


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1


class CharityProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectDB(SchemaBaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
