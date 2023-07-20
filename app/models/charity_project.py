from sqlalchemy import Column, String, Text

from app.models.abstract_base_model import AbstractBaseModel


class CharityProject(AbstractBaseModel):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
