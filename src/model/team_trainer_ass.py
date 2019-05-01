from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

from model.team import Team
from model.trainer import Trainer

Base = declarative_base()


class TeamTrainerAss(Base):
    __tablename__ = 'team_trainer_ass'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    team_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    trainer_id = Column(Integer, ForeignKey(Trainer.id), nullable=False)
    date = Column(Date, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.team_id
