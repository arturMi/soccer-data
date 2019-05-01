from sqlalchemy import Column, Integer, Date, VARCHAR, ForeignKey
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
    date = Column(Date, nullable=False)
    matchday = Column(Integer, nullable=False)
    home_team = Column(VARCHAR, nullable=False)
    away_team = Column(VARCHAR, nullable=False)
    goals_home_team = Column(Integer, nullable=False)
    goals_away_team = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return 'Spieltag' + self.matchday + self.date
