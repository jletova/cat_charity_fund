from sqlalchemy import (Column, String, Text,
                        Integer, DateTime, Boolean)
# from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f'Проект №{self.id}'
        )

    class Config:
        min_anystr_length = 1
