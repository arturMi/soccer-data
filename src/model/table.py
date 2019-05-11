from sqlalchemy import Column, Integer, JSON, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from model.season import Season

Base = declarative_base()


class Table(Base):
    __tablename__ = 'table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    table = Column(JSON, nullable=False)
    match_day = Column(Integer, nullable=False)
    season_id = Column(Integer, ForeignKey(Season.id), nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.date