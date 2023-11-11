from sqlalchemy import Column, Date, Float, Integer, String
from .base import BaseModel


class Unit(BaseModel):
    __tablename__ = "units"

    url = Column(String)
    name = Column(String)
    subject = Column(String)
    date_start = Column(Date)
    date_end = Column(Date)
    time_end = Column(Integer)
    passed_points = Column(Float)
    max_points = Column(Float)
    eval_method = Column(String)
    attempts = Column(Integer)
