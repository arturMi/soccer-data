from model.db import get_match_data, session_add, session_commit, check_league, check_team, check_trainer, get_trainer, \
    get_team, check_player, get_player
from model.season import Season
from model.league import League

from model.team import Team
from model.trainer import Trainer
from model.player import Player
from model.team_trainer_ass import TeamTrainerAss
from model.team_player_ass import TeamPlayerAss

from dateutil import parser


def parse():
    # Bundesliga hinzufügen, wenn keine vorhanden ist
    # Bundesliga
    l = "Bundesliga"
    c = 'Germany'
    y = 2017
    add_league_season(l, c, y)

    matches = get_match_data()
    for match in matches:
        # Spieler Team hinzufügen
        add_player_team(match)
        # Trainer Team hinzufügen
        add_trainer_team(match)
        # Event Match Report hinzufügen
        add_event_match_report(match)


def add_league_season(name, country, year):
    if not check_league(name):
        bl = League(name=name, country=country)
        session_add(bl)
        session_commit()
        # Saison zur Liga hinzufügen
        season = Season(league_id=bl.id, year=year)
        session_add(season)
        session_commit()


def add_player_team(match):
    #Heimspieler hinzufügen
    for player in match.doc["home"]["players"]:
        # Unique Player-ID
        home_player_id = player["playerId"]
        # Name
        home_player_name = player["name"]
        # Shirt Nummer
        home_player_shirt = player["shirtNo"]
        # Position
        home_player_position = player["position"]
        # Größe
        home_player_height = player["height"]
        # Gewicht
        home_player_weight = player["weight"]
        # Alter
        home_player_age = player["age"]

        # Spieler hinzufügen
        if not check_player(home_player_id):
            home_player = Player(id=home_player_id, name=home_player_name, shirt_number=home_player_shirt,
                                  position=home_player_position, height=home_player_height, weight=home_player_weight,
                                  age=home_player_age)
            session_add(home_player)
            session_commit()
        else:
            home_player = get_player(home_player_id)

    # Heim Team-ID und Team Name
    home_team_id = match.doc["home"]["teamId"]
    home_team_name = match.doc["home"]["name"]

    # Start des Spiels
    start_time = parser.parse(match.doc["startTime"])

    # Team hinzufügen
    if not check_team(home_team_id):
        home_team = Team(id=home_team_id, team_name=home_team_name)
        session_add(home_team)
        session_commit()
    else:
        home_team = get_team(home_team_id)

    # Beziehung hinzufügen
    asso = TeamPlayerAss(team_id=home_team.id, player_id=home_player.id, date=start_time)
    session_add(asso)
    session_commit()

    # Auswärtsspieler hinzufügen
    for player in match.doc["away"]["players"]:
        # Unique Player-ID
        away_player_id = player["playerId"]
        # Name
        away_player_name = player["name"]
        # Shirt Nummer
        away_player_shirt = player["shirtNo"]
        # Position
        away_player_position = player["position"]
        # Größe
        away_player_height = player["height"]
        # Gewicht
        away_player_weight = player["weight"]
        # Alter
        away_player_age = player["age"]

        # Spieler hinzufügen
        if not check_player(away_player_id):
            away_player = Player(id=away_player_id, name=away_player_name, shirt_number=away_player_shirt,
                                 position=away_player_position, height=away_player_height, weight=away_player_weight,
                                 age=away_player_age)
            session_add(away_player)
            session_commit()
        else:
            away_player = get_player(away_player_id)

    # Auswärts Team-ID und Team Name
    away_team_id = match.doc["away"]["teamId"]
    away_team_name = match.doc["away"]["name"]

    # Start des Spiels
    start_time = parser.parse(match.doc["startTime"])

    # Team hinzufügen
    if not check_team(away_team_id):
        away_team = Team(id=away_team_id, team_name=away_team_name)
        session_add(away_team)
        session_commit()
    else:
        away_team = get_team(away_team_id)

    # Beziehung hinzufügen
    asso = TeamPlayerAss(team_id=away_team.id, player_id=away_player.id, date=start_time)
    session_add(asso)
    session_commit()

def add_trainer_team(match):
    # Trainername des Heimteams
    home_team_trainer = match.doc["home"]["managerName"]

    # Heim Team-ID und Team Name
    home_team_id = match.doc["home"]["teamId"]
    home_team_name = match.doc["home"]["name"]

    # Start des Spiels
    start_time = parser.parse(match.doc["startTime"])

    # Trainer hinzufügen
    if not check_trainer(home_team_trainer):
        home_trainer = Trainer(name=home_team_trainer)
        session_add(home_trainer)
        session_commit()
    else:
        home_trainer = get_trainer(home_team_trainer)

    # Team hinzufügen
    if not check_team(home_team_id):
        home_team = Team(id=home_team_id, team_name=home_team_name)
        session_add(home_team)
        session_commit()
    else:
        home_team = get_team(home_team_id)

    # Beziehung hinzufügen
    asso = TeamTrainerAss(team_id=home_team.id, trainer_id=home_trainer.id, date=start_time)
    session_add(asso)
    session_commit()

    # Trainername des Auswärtsteams
    away_team_trainer = match.doc["away"]["managerName"]

    # Auswärts Team-ID und Team Name
    away_team_id = match.doc["away"]["teamId"]
    away_team_name = match.doc["away"]["name"]

    # Start des Spiels
    start_time = parser.parse(match.doc["startTime"])

    # Trainer hinzufügen
    if not check_trainer(away_team_trainer):
        away_trainer = Trainer(name=away_team_trainer)
        session_add(away_trainer)
        session_commit()
    else:
        away_trainer = get_trainer(away_team_trainer)

    # Team hinzufügen
    if not check_team(away_team_id):
        away_team = Team(id=away_team_id, team_name=away_team_name)
        session_add(away_team)
        session_commit()
    else:
        away_team = get_team(away_team_id)

    # Beziehung hinzufügen
    asso = TeamTrainerAss(team_id=away_team.id, trainer_id=away_trainer.id, date=start_time)
    session_add(asso)
    session_commit()

def add_event_match_report(match):
    print("Gute Report")