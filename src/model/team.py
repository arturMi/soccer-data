from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    team_name = Column(VARCHAR, nullable=False)
    city = Column(VARCHAR, nullable=False)
