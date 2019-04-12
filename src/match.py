from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Match(Base):

    __tablename__ = 'match'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    matchday = Column(Integer)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)