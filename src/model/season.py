from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Season(Base):
    __tablename__ = 'season'

    id = Column(Integer, primary_key=True, autoincrement=True)
    league = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.league + self.year
