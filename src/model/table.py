from sqlalchemy import Column, Integer, VARCHAR, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Table(Base):
    __tablename__ = 'table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    table = Column(VARCHAR, nullable=False)
    match_day = Column(Integer, nullable=False)
    season_id = Column(Integer, nullable=False, ForeignKey('season.id'))

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.date