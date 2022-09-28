from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    class Config:
        min_anystr_length = 1

    def __repr__(self):
        return (
            f'Donation from user #{self.user_id}: {self.full_amount}'
        )
