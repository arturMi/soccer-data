from sqlalchemy import Column, Integer, JSON, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    teamId = Column(Integer, nullable=False)
    data = Column(JSON, nullable=False)
    type = Column(VARCHAR)
    outcome_successful = Column(bool)
    minute = Column(Integer)
    second = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)


    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.league + self.teamId