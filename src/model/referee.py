from sqlalchemy import Column, Integer, VARCHAR, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Referee(Base):
    __tablename__ = 'referee'

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.first_name