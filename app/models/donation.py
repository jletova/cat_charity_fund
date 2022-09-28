from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base_model import ProjectBaseModel


class Donation(ProjectBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String)

    class Config:
        min_anystr_length = 1

    def __repr__(self):
        return (
            f'Donation from user #{self.user_id}: {self.full_amount}'
        )
