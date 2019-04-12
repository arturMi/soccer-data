from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MatchReport(Base):

    __tablename__ = 'match_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_day = Column(Integer, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    total_shots_home = Column (Integer)
    total_shots_away = Column(Integer)
    posession_home = Column(Integer, nullable=False)
    possesion_away = Column(Integer, nullable=False)
    pass_success_home = Column(Integer, nullable=False)
    pass_success_away = Column(Integer, nullable=False)
    dribbles_home = Column(Integer, nullable=False)
    dribbles_away = Column(Integer, nullable=False)
    aerials_won_home = Column(Integer, nullable=False)
    aerials_won_away = Column(Integer, nullable=False)
    tackles_home = Column(Integer, nullable=False)
    tackles_away = Column(Integer, nullable=False)
    corners_home = Column(Integer, nullable=False)
    corners_away = Column(Integer, nullable=False)