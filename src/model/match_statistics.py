from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MatchStatistics(Base):
    __tablename__ = 'match_statistics'

    # columns serial, String, json
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    text = Column(String)
    doc = Column(JSON)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.text
