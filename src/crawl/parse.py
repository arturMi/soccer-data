from model.db import get_match_data, session_add, session_commit, check_league, check_team, check_trainer, get_trainer, \
    get_team, check_player, get_player, check_event, get_event, check_report, get_report, check_match, get_match, \
    get_league, get_season
from model.season import Season
from model.league import League

from model.team import Team
from model.trainer import Trainer
from model.player import Player
from model.event import Event
from model.match import Match
from model.match_report import MatchReport
from model.team_trainer_ass import TeamTrainerAss
from model.team_player_ass import TeamPlayerAss
from model.match_repor_event_ass import MatchReportAss

import json
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
        # add_trainer_team(match)
        # Match hinzufügen
        # add_match(match)
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

    # Heimspieler hinzufügen
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
        # Statistik
        home_player_statistics = json.dumps(player["stats"])

        # Spieler hinzufügen
        if not check_player(home_player_id):
            home_player = Player(id=home_player_id, name=home_player_name)
            session_add(home_player)
            session_commit()
        else:
            home_player = get_player(home_player_id)

        # Beziehung hinzufügen
        asso = TeamPlayerAss(team_id=home_team.id, player_id=home_player.id, date=start_time,
                             shirt_number=home_player_shirt, position=home_player_position, height=home_player_height,
                             weight=home_player_weight, age=home_player_age, stat_doc=home_player_statistics)
        session_add(asso)
        session_commit()

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
        # Statistik
        away_player_statistics = json.dumps(player["stats"])

        # Spieler hinzufügen
        if not check_player(away_player_id):
            away_player = Player(id=away_player_id, name=away_player_name)
            session_add(away_player)
            session_commit()
        else:
            away_player = get_player(away_player_id)

        # Beziehung hinzufügen
        asso = TeamPlayerAss(team_id=away_team.id, player_id=away_player.id, date=start_time,
                             shirt_number=away_player_shirt,
                             position=away_player_position, height=away_player_height, weight=away_player_weight,
                             age=away_player_age, statics_doc=away_player_statistics)
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
    home_team = match.doc["home"]["name"]
    away_team = match.doc["away"]["name"]
    score_halftime = match.doc["score"]
    score_final = match.doc["htScore"]
    start_time = parser.parse(match.doc["startTime"])
    stadion = match.doc["venueName"]
    home_team_id = match.doc["home"]["teamId"]
    away_team_id = match.doc["away"]["teamId"]
    league = get_league("Bundesliga")
    season_id = get_season(2017, league.id).id

    # Spieler hinzufügen
    match_game = Match(home_team=home_team, season_id=season_id, away_team=away_team, away_team_id=away_team_id,
                       home_team_id=home_team_id, score_ht=score_halftime, score=score_final,
                       date=start_time, location=stadion, referee_id=referee_id)
    session_add(match_game)
    session_commit()

    # Event hinzufügen
    for event in match.doc["events"]:
        #event_id = event["id"]
        team_id = event["teamId"]
        minute = event["minute"]
        if "second" in event:
            second = event["second"]
        else:
            second = 0
        event_type = event["type"]["displayName"]
        event_outcome = event["outcomeType"]["displayName"]
        x_coord = event["x"]
        y_coord = event["y"]
        event_doc = event

        if event_outcome == "Successful":
            event_outcome = True
        else:
            event_outcome = False


        event = Event(team_id=team_id, minute=minute, second=second, type=event_type,
                        outcome_successful=event_outcome, x=x_coord, y=y_coord, data=event_doc)
        session_add(event)
        session_commit()


    # Report Heim

    home_average_age = match.doc["home"]["averageAge"]
    home_scores = match.doc["home"]["scores"]["fulltime"]
    home_scores_halftime = match.doc["home"]["scores"]["halftime"]

    # Report Auswärts

    away_average_age = match.doc["away"]["averageAge"]
    away_scores = match.doc["away"]["scores"]["fulltime"]
    away_scores_halftime = match.doc["away"]["scores"]["halftime"]

    # Match Report hinzufügen

    match_report = MatchReport(home_scores=home_scores, home_scores_ht=home_scores_halftime,
                               away_scores=away_scores, away_scores_ht=away_scores_halftime,
                               home_average_age=home_average_age, away_average_age=away_average_age,
                               website="whoscored.com", match_id=match_game.id)
    session_add(match_report)
    session_commit()

    # Beziehung hinzufügen
    asso = MatchReportAss(event_id=event.id, match_report_id=match_report.id)
    session_add(asso)
    session_commit()

