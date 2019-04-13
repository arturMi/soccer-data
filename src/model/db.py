from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model.config import SQLALCHEMY_DATABASE_URI
import atexit
import ast

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


# def save_game_to_database(txt, json):
#  game = MatchStatistics(text=txt, doc=json)
#  session.add(game)
#  session.commit()


def get_match_day_data(season):
    """
        Get all the match day data
    """
    seasons = session.query(MatchDayData).filter(MatchDayData.season == season).all()
    return seasons


def get_match_data():
    """
        Get all the match day data
    """
    matches = session.query(MatchStatistics).all()
    return matches


def session_commit():
    """
        commit the session data
    """
    session.commit()


def generate_game_url(season):
    """
        Build the game url
    """
    seasons = get_match_day_data(season)
    for match_day in seasons:
        data_list = ast.literal_eval(match_day.data)
        for match in data_list:
            url = 'https://www.whoscored.com/Matches/' + str(match[0]) + '/Live'
            game = MatchStatistics(url=url)
            session.add(game)
    session.commit()


def remove_session():
    """
        Remove the session
    """
    session.remove()


atexit.register(remove_session)
