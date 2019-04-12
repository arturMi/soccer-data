from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    matchday = Column(Integer, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    goals_home_team = Column(Integer, nullable=False)
    goals_away_team = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return 'Spieltag' + self.matchday + self.date