from sqlalchemy import Column, String, Text

from app.models.base_model import ProjectBaseModel


class CharityProject(ProjectBaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    class Config:
        min_anystr_length = 1

    def __repr__(self):
        return (
            f'Project №{self.id}'
        )
