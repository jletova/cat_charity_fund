from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Extra, Field, PositiveInt,
                      NonNegativeInt, validator)


# class QRKotBaseModel(BaseModel):
#     full_amount: Optional[int] = Field(..., gt=0)
#     invested_amount: Optional[int] = 0
#     fully_invested: Optional[bool] = False
#     create_date: Optional[datetime] = datetime.now()
#     close_date: Optional[datetime]


class QRKotBaseModel(BaseModel):
    __abstract__ = True
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
    name: Optional[str] = Field(..., max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectDB(QRKotBaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str

    class Config:
        orm_mode = True
