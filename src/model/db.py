from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model.config import SQLALCHEMY_DATABASE_URI

# import all table-files
from model.match_statistics import MatchStatistics
from model.match_day_data import MatchDayData
from model.match import Match
from model.season import Season
from model.match_report import MatchReport
from model.team import Team
from model.table import Table
from model.trainer import Trainer
from model.player import Player

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker())
session.configure(bind=engine, autoflush=False, expire_on_commit=False)


def create_tables():
    """
        Create all tables
    """
    MatchStatistics.__table__.create(engine)
    Match.__table__.create(engine)
    Season.__table__.create(engine)
    MatchReport.__table__.create(engine)
    Team.__table__.create(engine)
    Table.__table__.create(engine)
    Trainer.__table__.create(engine)
    Player.__table__.create(engine)
    MatchDayData.__table__.create(engine)

    session.commit()

    session.remove()


def save_game_to_database(txt, json):
    """
        Save game to database raw
    """
    game = MatchStatistics(text=txt, doc=json)
    session.add(game)
    session.commit()


def print_season(season):
    """
        Print all match day data from season
    """
    season = session.query(MatchDayData).filter(MatchDayData.season == season).all()
    for day in season:
        print(day)
    session.remove()
