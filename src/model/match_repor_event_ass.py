from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MatchReportAss(Base):
    __tablename__ = 'match_repor_event_ass'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    match_report_id = Column(Integer, ForeignKey('match_report.id'), nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.event_id