from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MatchDay(Base):

    __tablename__ = 'match_day'

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_day = Column(Integer, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)