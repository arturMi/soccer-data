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
from model.event import Event
from model.league import League
from model.match_repor_event_ass import MatchReportAss
from model.team_player_ass import TeamPlayerAss
from model.team_trainer_ass import TeamTrainerAss

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
    Event.__table__.create(engine)
    League.__table__.create(engine)
    MatchReportAss.__table__.create(engine)
    TeamPlayerAss.__table__.create(engine)
    TeamTrainerAss.__table__.create(engine)

    session.commit()


# def save_game_to_database(txt, json):
#  game = MatchStatistics(text=txt, doc=json)
#  session.add(game)
#  session.commit()


def get_match_day_data(season):
    """
        Query um alle Spieltag Daten zu bekommen
    """
    seasons = session.query(MatchDayData).filter(MatchDayData.season == season).all()
    return seasons


def get_match_data():
    """
        Query um alle Spieltage zu bekommen
    """
    matches = session.query(MatchStatistics).all()
    return matches


def session_commit():
    """
        Absichern der Session
    """
    session.commit()


def session_add(obj):
    """
        Objekt zur Session hinzufügen
    """
    session.add(obj)


def generate_game_url(season):
    """
        Erstellen der Spiel-URL
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
        Session beenden
    """
    session.remove()


def check_league(name):
    """
        Liga prüfen
    """
    return session.query(League).filter(League.name == name).count()


def check_trainer(name):
    """
        Trainer prüfen
    """
    return session.query(Trainer).filter(Trainer.name == name).count()


def get_trainer(name):
    """
        Name des Trainers holen
    """
    return session.query(Trainer).filter(Trainer.name == name).first()

def check_player(id):
    """
        Spieler prüfen
    """
    return session.query(Trainer).filter(Player.id == id).count()

def get_player(id):
    """
        Spieler ID holen
    """
    return session.query(Player).filter(Player.id == id).first()

def check_team(id):
    """
        Team prüfen
    """
    return session.query(Team).filter(Team.id == id).count()


def get_team(id):
    """
        Team ID holen
    """
    return session.query(Team).filter(Team.id == id).first()


atexit.register(remove_session)
