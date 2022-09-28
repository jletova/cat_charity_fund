from typing import Optional
from app.schemas.charity_project import QRKotBaseModel
from pydantic import BaseModel, Extra


class DonationCreate(BaseModel):
    full_amount: int
    comment: str

    class Config:
        extra = Extra.forbid


class DonationDB(QRKotBaseModel):
    id: int
    comment: Optional[str]
    user_id: Optional[int]

    class Config:
        orm_mode = True
