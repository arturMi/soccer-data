from sqlalchemy import Column, Integer, String, Date, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.first_name + self.name