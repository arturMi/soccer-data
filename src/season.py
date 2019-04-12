from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Season(Base):

    __tablename__ = 'season'

    id = Column(Integer, primary_key=True, autoincrement=True)
    league = Column(String, nullable=False)
    year = Column(Integer, nullable=False)