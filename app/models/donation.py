from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract_base_model import AbstractBaseModel


class Donation(AbstractBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
