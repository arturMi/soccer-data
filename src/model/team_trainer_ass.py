from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TeamTrainerAss(Base):
    __tablename__ = 'team_trainer_ass'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    team_id = Column(Integer, nullable=False, ForeignKey('team.id')
    trainer_id = Column(Integer, nullable=False, ForeignKey('trainer.id'))

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.team_id