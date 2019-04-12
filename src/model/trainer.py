from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Trainer(Base):
    __tablename__ = 'trainer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    nationality = Column(String, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.first_name + self.name