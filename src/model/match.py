from sqlalchemy import Column, Integer, Date, VARCHAR, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

from model.season import Season
from model.team import Team

Base = declarative_base()


class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True, autoincrement=True)
    season_id = Column(Integer, ForeignKey(Season.id), nullable=False)
    home_team_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    away_team_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    date = Column(Date)
    matchday = Column(Integer)
    home_team = Column(VARCHAR)
    away_team = Column(VARCHAR)
    score_ht = Column(VARCHAR)
    score = Column(VARCHAR)
    location = Column(VARCHAR)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return 'Spieltag' + self.matchday + self.date
