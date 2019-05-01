from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MatchReport(Base):
    __tablename__ = 'match_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    website = Column(String, nullable=False)
    match_id = Column(Integer, ForeignKey('match.id'), nullable=False)
    total_shots_home = Column(Integer)
    total_shots_away = Column(Integer)
    posession_home = Column(Integer)
    possesion_away = Column(Integer)
    pass_success_home = Column(Integer)
    pass_success_away = Column(Integer)
    dribbles_home = Column(Integer)
    dribbles_away = Column(Integer)
    aerials_won_home = Column(Integer)
    aerials_won_away = Column(Integer)
    tackles_home = Column(Integer)
    tackles_away = Column(Integer)
    corners_home = Column(Integer)
    corners_away = Column(Integer)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.website