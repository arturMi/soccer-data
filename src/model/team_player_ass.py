from sqlalchemy import Column, Integer, ForeignKey, Date, VARCHAR, JSON
from sqlalchemy.ext.declarative import declarative_base

from model.team import Team
from model.player import Player

Base = declarative_base()


class TeamPlayerAss(Base):
    __tablename__ = 'team_player_ass'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    team_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    player_id = Column(Integer, ForeignKey(Player.id), nullable=False)
    date = Column(Date, nullable=False)
    shirt_number = Column(VARCHAR)
    position = Column(VARCHAR)
    height = Column(Integer)
    weight = Column(Integer)
    age = Column(Integer)
    stat_doc = Column(JSON)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.team_id