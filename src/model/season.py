from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from model.league import League

Base = declarative_base()


class Season(Base):
    __tablename__ = 'season'

    # relationships

    id = Column(Integer, primary_key=True, autoincrement=True)
    league_id = Column(Integer, ForeignKey(League.id), nullable=False)
    # ParentID = Column('CompanyID', Integer, ForeignKey(Parent.ParentID))
    # league = relationship(League, backref=backref("league", cascade="all, delete-orphan"))
    year = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.league + self.year
