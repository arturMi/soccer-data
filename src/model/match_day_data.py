from sqlalchemy import Column, VARCHAR, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MatchDayData(Base):
    __tablename__ = 'match_day_data'

    match_day_url = Column(String, primary_key=True)
    crawled = Column(Boolean, nullable=False)
    season = Column(VARCHAR, nullable=False)
    match_day = Column(Integer, nullable=False)
    data = Column(String)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.match_day_url