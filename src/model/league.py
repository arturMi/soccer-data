from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class League(Base):
    __tablename__ = 'league'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR, nullable=False)
    country = Column(VARCHAR)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.league + self.year