from model.db import get_match_data, session_add, session_commit, check_league, check_team, check_trainer, get_trainer, \
    get_team, check_player, get_player, get_league, get_season, check_referee, get_referee
from model.season import Season
from model.league import League

from model.team import Team
from model.trainer import Trainer
from model.player import Player
from model.event import Event
from model.match import Match
from model.referee import Referee
from model.match_report import MatchReport
from model.team_trainer_ass import TeamTrainerAss
from model.team_player_ass import TeamPlayerAss
from model.match_repor_event_ass import MatchReportAss
from dateutil import parser

import json


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
        # Add Referee
        add_referee(match)
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
    if "home" in match.doc:
        if "teamId" in match.doc["home"]:
            home_team_id = match.doc["home"]["teamId"]
        else:
            print("No value in home.teamId")
        if "name" in match.doc["home"]:
            home_team_name = match.doc["home"]["name"]
        else:
            print("No value in name")
    else:
        print("No value in home")

    # Start des Spiels
    if "startTime" in match.doc:
        start_time = parser.parse(match.doc["startTime"])
    else:
        print("No value in startTime")

    # Team hinzufügen
    if not check_team(home_team_id):
        home_team = Team(id=home_team_id, team_name=home_team_name)
        session_add(home_team)
        session_commit()
    else:
        home_team = get_team(home_team_id)

    # Heimspieler hinzufügen
        if "players" in match.doc["home"]:
            for player in match.doc["home"]["players"]:
                if "playerId" in match.doc["home"]["players"]:
                    # Unique Player-ID
                    home_player_id = player["playerId"]
                else:
                    home_player_id = json.dumps({})
                    print("No playerId in home given.")
                if "name" in match.doc["home"]["players"]:
                    # Name
                    home_player_name = player["name"]
                else:
                    home_player_name = json.dumps({})
                    print("No name in home given.")
                if "shirtNo" in match.doc["home"]["players"]:
                    # Shirt Nummer
                    home_player_shirt = player["shirtNo"]
                else:
                    home_player_shirt = json.dumps({})
                    print("No shirtNo in home given.")
                if "position" in match.doc["home"]["players"]:
                    # Position
                    home_player_position = player["position"]
                else:
                    home_player_position = json.dumps({})
                    print("No position in home given.")
                if "height" in match.doc["home"]["players"]:
                    # Größe
                    home_player_height = player["height"]
                else:
                    home_player_height = json.dumps({})
                    print("No height in home given.")
                if "weight" in match.doc["home"]["players"]:
                    # Gewicht
                    home_player_weight = player["weight"]
                else:
                    home_player_weight = json.dumps({})
                    print("No weight in home given.")
                if "age" in match.doc["home"]["players"]:
                    # Alter
                    home_player_age = player["age"]
                else:
                    home_player_age = json.dumps({})
                    print("No age in home given")
                if "stats" in match.doc["home"]["players"]:
                    # Statistik
                    home_player_statistics = json.dumps(player["stats"])
                else:
                    home_player_statistics = json.dumps({})
                    print("No stats in home given.")
        else:
            print("No players in home given.")

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
    if "away" in match.doc:
        if "teamId" in match.doc["away"]:
            away_team_id = match.doc["away"]["teamId"]
        else:
            print("No teamId in away.")
        if "name" in match.doc["away"]:
            away_team_name = match.doc["away"]["name"]
        else:
            print("No name in away.")
    else:
        print("No away team given.")

    # Start des Spiels
    if "startTime" in match.doc:
        start_time = parser.parse(match.doc["startTime"])
    else:
        print("No startTime given.")

    # Team hinzufügen
    if not check_team(away_team_id):
        away_team = Team(id=away_team_id, team_name=away_team_name)
        session_add(away_team)
        session_commit()
    else:
        away_team = get_team(away_team_id)

    # Auswärtsspieler hinzufügen
        if "players" in match.doc["away"]:
            for player in match.doc["away"]["players"]:
                if "playerId" in match.doc["away"]["players"]:
                    # Unique Player-ID
                    away_player_id = player["playerId"]
                else:
                    away_player_id = json.dumps({})
                    print("No playerId in away given.")
                if "name" in match.doc["away"]["players"]:
                    # Name
                    away_player_name = player["name"]
                else:
                    away_player_name = json.dumps({})
                    print("No name in away given.")
                if "shirtNo" in match.doc["away"]["players"]:
                    # Shirt Nummer
                    away_player_shirt = player["shirtNo"]
                else:
                    away_player_shirt = json.dumps({})
                    print("No shirtNo in away given.")
                if "position" in match.doc["away"]["players"]:
                    # Position
                    away_player_position = player["position"]
                else:
                    away_player_position = json.dumps({})
                    print("No position in away given.")
                if "height" in match.doc["away"]["players"]:
                    # Größe
                    away_player_height = player["height"]
                else:
                    away_player_height = json.dumps({})
                    print("No height in away given.")
                if "weight" in match.doc["away"]["players"]:
                    # Gewicht
                    away_player_weight = player["weight"]
                else:
                    away_player_weight = json.dumps({})
                    print("No weight in away given.")
                if "age" in match.doc["away"]["players"]:
                    # Alter
                    away_player_age = player["age"]
                else:
                    away_player_age = json.dumps({})
                    print("No age in away given")
                if "stats" in match.doc["away"]["players"]:
                    # Statistik
                    away_player_statistics = json.dumps(player["stats"])
                else:
                    away_player_statistics = json.dumps({})
                    print("No stats in away given.")
        else:
            print("No players in away given.")

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
                             age=away_player_age, stat_doc=away_player_statistics)
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
    score_final = match.doc["score"]
    score_halftime = match.doc["htScore"]
    start_time = parser.parse(match.doc["startTime"])
    stadion = match.doc["venueName"]
    home_team_id = match.doc["home"]["teamId"]
    away_team_id = match.doc["away"]["teamId"]
    league = get_league("Bundesliga")
    season_id = get_season(2017, league.id).id

    if "referee" in match.doc:
        referee_id = match.doc["referee"]["officialId"]
        match_game = Match(home_team=home_team, season_id=season_id, away_team=away_team, away_team_id=away_team_id,
                           home_team_id=home_team_id, score_ht=score_halftime, score=score_final,
                           date=start_time, location=stadion, referee_id=referee_id)
    else:
        match_game = Match(home_team=home_team, season_id=season_id, away_team=away_team, away_team_id=away_team_id,
                           home_team_id=home_team_id, score_ht=score_halftime, score=score_final,
                           date=start_time, location=stadion)
    session_add(match_game)
    session_commit()

    # Event hinzufügen
    for event in match.doc["events"]:
        # event_id = event["id"]
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

        event = Event(team_id=team_id, minute=minute, second=second, type=event_type, outcome_successful=event_outcome,
                      x=x_coord, y=y_coord, data=event_doc)
        session_add(event)
        session_commit()

    # Matchreport Heim
    if "home" in match.doc:
        if "averageAge" in match.doc["home"]:
            home_average_age = match.doc["home"]["averageAge"]
        else:
            home_average_age = json.dumps({})
            print("No averageAge value given.")
        if "scores" in match.doc["home"]:
            if "fulltime" in match.doc["home"]["scores"]:
                home_scores = match.doc["home"]["scores"]["fulltime"]
            else:
                home_scores = json.dumps({})
                print("No fulltime in scores given.")
            if "halftime" in match.doc["home"]["scores"]:
                home_scores_halftime = match.doc["home"]["scores"]["halftime"]
            else:
                home_scores_halftime = json.dumps({})
                print("No halftime in scores given.")
        else:
            print("No scores in home.")
        if "stats" in match.doc["home"]:
            if "ratings" in match.doc["home"]["stats"]:
                home_ratings = json.dumps(match.doc["home"]["stats"]["ratings"])
            else:
                home_ratings = json.dumps({})
                print("No ratings in stats given.")
            if "shotsTotal" in match.doc["home"]["stats"]:
                home_shots_total = json.dumps(match.doc["home"]["stats"]["shotsTotal"])
            else:
                home_shots_total = json.dumps({})
                print("No value in home given.")
            if "shotsOnTarget" in match.doc["home"]["stats"]:
                home_shots_on_target = json.dumps(match.doc["home"]["stats"]["shotsOnTarget"])
            else:
                home_shots_on_target = json.dumps({})
                print("No value in home given.")
            if "shotsOffTarget" in match.doc["home"]["stats"]:
                home_shots_off_target = json.dumps(match.doc["home"]["stats"]["shotsOffTarget"])
            else:
                home_shots_off_target = json.dumps({})
                print("No value in home given.")
            if "shotsBlocked" in match.doc["home"]["stats"]:
                home_shots_blocked = json.dumps(match.doc["home"]["stats"]["shotsBlocked"])
            else:
                home_shots_blocked = json.dumps({})
                print("No value in home given.")
            if "clearances" in match.doc["home"]["stats"]:
                home_clearances = json.dumps(match.doc["home"]["stats"]["clearances"])
            else:
                home_clearances = json.dumps({})
                print("No value in home given.")
            if "interceptions" in match.doc["home"]["stats"]:
                home_interceptions = json.dumps(match.doc["home"]["stats"]["interceptions"])
            else:
                home_interceptions = json.dumps({})
                print("No value in home given.")
            if "possession" in match.doc["home"]["stats"]:
                home_possesion = json.dumps(match.doc["home"]["stats"]["possession"])
            else:
                home_possesion = json.dumps({})
                print("No value in home given.")
            if "touches" in match.doc["home"]["stats"]:
                home_touches = json.dumps(match.doc["home"]["stats"]["touches"])
            else:
                home_touches = json.dumps({})
                print("No value in home given.")
            if "passesTotal" in match.doc["home"]["stats"]:
                home_passes_total = json.dumps(match.doc["home"]["stats"]["passesTotal"])
            else:
                home_passes_total = json.dumps({})
                print("No value in home given.")
            if "passesAccurate" in match.doc["home"]["stats"]:
                home_passes_accurate = json.dumps(match.doc["home"]["stats"]["passesAccurate"])
            else:
                home_passes_accurate = json.dumps({})
                print("No value in home given.")
            if "passesKey" in match.doc["home"]["stats"]:
                home_passes_key = json.dumps(match.doc["home"]["stats"]["passesKey"])
            else:
                home_passes_key = json.dumps({})
                print("No value in home given.")
            if "passSuccess" in match.doc["home"]["stats"]:
                home_pass_success = json.dumps(match.doc["home"]["stats"]["passSuccess"])
            else:
                home_pass_success = json.dumps({})
                print("No value in home given.")
            if "aerialsTotal" in match.doc["home"]["stats"]:
                home_aerials_total = json.dumps(match.doc["home"]["stats"]["aerialsTotal"])
            else:
                home_aerials_total = json.dumps({})
                print("No value in home given.")
            if "aerialsWon" in match.doc["home"]["stats"]:
                home_aerials_won = json.dumps(match.doc["home"]["stats"]["aerialsWon"])
            else:
                home_aerials_won = json.dumps({})
                print("No value in home given.")
            if "aerialSuccess" in match.doc["home"]["stats"]:
                home_aerials_success = json.dumps(match.doc["home"]["stats"]["aerialSuccess"])
            else:
                home_aerials_success = json.dumps({})
                print("No value in home given.")
            if "offensiveAerials" in match.doc["home"]["stats"]:
                home_offensive_aerials = json.dumps(match.doc["home"]["stats"]["offensiveAerials"])
            else:
                home_offensive_aerials = json.dumps({})
                print("No value in home given.")
            if "defensiveAerials" in match.doc["home"]["stats"]:
                home_defensive_aerials = json.dumps(match.doc["home"]["stats"]["defensiveAerials"])
            else:
                home_defensive_aerials = json.dumps({})
                print("No value in home given.")
            if "cornersTotal" in match.doc["home"]["stats"]:
                home_corners_total = json.dumps(match.doc["home"]["stats"]["cornersTotal"])
            else:
                home_corners_total = json.dumps({})
                print("No value in home given.")
            if "throwInsTotal" in match.doc["home"]["stats"]:
                home_throw_ins_total = json.dumps(match.doc["home"]["stats"]["throwInsTotal"])
            else:
                home_throw_ins_total = json.dumps({})
                print("No value in home given.")
            if "throwInsAccurate" in match.doc["home"]["stats"]:
                home_throw_ins_accurate = json.dumps(match.doc["home"]["stats"]["throwInsAccurate"])
            else:
                home_throw_ins_accurate = json.dumps({})
                print("No value in home given.")
            if "foulsCommited" in match.doc["home"]["stats"]:
                home_fouls_commited = json.dumps(match.doc["home"]["stats"]["foulsCommited"])
            else:
                home_fouls_commited = json.dumps({})
                print("No value in home given.")
            if "tacklesTotal" in match.doc["home"]["stats"]:
                home_tackles_total = json.dumps(match.doc["home"]["stats"]["tacklesTotal"])
            else:
                home_tackles_total = json.dumps({})
                print("No value in home given.")
            if "tackleSuccessful" in match.doc["home"]["stats"]:
                home_tackles_successful = json.dumps(match.doc["home"]["stats"]["tackleSuccessful"])
            else:
                home_tackles_successful = json.dumps({})
                print("No value in home given.")
            if "tackleUnsuccesful" in match.doc["home"]["stats"]:
                home_tackles_unsuccessful = json.dumps(match.doc["home"]["stats"]["tackleUnsuccesful"])
            else:
                home_tackles_unsuccessful = json.dumps({})
                print("No value in home given.")
            if "tackleSuccess" in match.doc["home"]["stats"]:
                home_tackles_success = json.dumps(match.doc["home"]["stats"]["tackleSuccess"])
            else:
                home_tackles_success = json.dumps({})
                print("No value in home given.")
            if "dribbledPast" in match.doc["home"]["stats"]:
                home_dribbled_past = json.dumps(match.doc["home"]["stats"]["dribbledPast"])
            else:
                home_dribbled_past = json.dumps({})
                print("No value in home given.")
            if "dribblesWon" in match.doc["home"]["stats"]:
                home_dribbles_won = json.dumps(match.doc["home"]["stats"]["dribblesWon"])
            else:
                home_dribbles_won = json.dumps({})
                print("No value in home given.")
            if "dribblesAttempted" in match.doc["home"]["stats"]:
                home_dribbles_attempted = json.dumps(match.doc["home"]["stats"]["dribblesAttempted"])
            else:
                home_dribbles_attempted = json.dumps({})
                print("No value in home given.")
            if "dribblesLost" in match.doc["home"]["stats"]:
                home_dribbles_lost = json.dumps(match.doc["home"]["stats"]["dribblesLost"])
            else:
                home_dribbles_lost = json.dumps({})
                print("No value in home given.")
            if "dribbleSuccess" in match.doc["home"]["stats"]:
                home_dribble_success = json.dumps(match.doc["home"]["stats"]["dribbleSuccess"])
            else:
                home_dribble_success = json.dumps({})
                print("No value in home given.")
            if "dispossessed" in match.doc["home"]["stats"]:
                home_dispossessed = json.dumps(match.doc["home"]["stats"]["dispossessed"])
            else:
                home_dispossessed = json.dumps({})
                print("No value in home given.")
        else:
            print("No stats in home.")
    else:
        print("No home value given.")

    # Matchreport Auswärts
    if "away" in match.doc:
        if "averageAge" in match.doc["away"]:
            away_average_age = match.doc["away"]["averageAge"]
        else:
            away_average_age = json.dumps({})
            print("No averageAge value given.")
        if "scores" in match.doc["away"]:
            if "fulltime" in match.doc["away"]["scores"]:
                away_scores = match.doc["away"]["scores"]["fulltime"]
            else:
                away_scores = json.dumps({})
                print("No fulltime in scores given.")
            if "halftime" in match.doc["away"]["scores"]:
                away_scores_halftime = match.doc["away"]["scores"]["halftime"]
            else:
                away_scores_halftime = json.dumps({})
                print("No halftime in scores given.")
        else:
            print("No scores in away.")
        if "stats" in match.doc["away"]:
            if "ratings" in match.doc["away"]["stats"]:
                away_ratings = json.dumps(match.doc["away"]["stats"]["ratings"])
            else:
                away_ratings = json.dumps({})
                print("No ratings in stats given.")
            if "shotsTotal" in match.doc["away"]["stats"]:
                away_shots_total = json.dumps(match.doc["away"]["stats"]["shotsTotal"])
            else:
                away_shots_total = json.dumps({})
                print("No value in away given.")
            if "shotsOnTarget" in match.doc["away"]["stats"]:
                away_shots_on_target = json.dumps(match.doc["away"]["stats"]["shotsOnTarget"])
            else:
                away_shots_on_target = json.dumps({})
                print("No value in away given.")
            if "shotsOffTarget" in match.doc["away"]["stats"]:
                away_shots_off_target = json.dumps(match.doc["away"]["stats"]["shotsOffTarget"])
            else:
                away_shots_off_target = json.dumps({})
                print("No value in away given.")
            if "shotsBlocked" in match.doc["away"]["stats"]:
                away_shots_blocked = json.dumps(match.doc["away"]["stats"]["shotsBlocked"])
            else:
                away_shots_blocked = json.dumps({})
                print("No value in away given.")
            if "clearances" in match.doc["away"]["stats"]:
                away_clearances = json.dumps(match.doc["away"]["stats"]["clearances"])
            else:
                away_clearances = json.dumps({})
                print("No value in away given.")
            if "interceptions" in match.doc["away"]["stats"]:
                away_interceptions = json.dumps(match.doc["away"]["stats"]["interceptions"])
            else:
                away_interceptions = json.dumps({})
                print("No value in away given.")
            if "possession" in match.doc["away"]["stats"]:
                away_possesion = json.dumps(match.doc["away"]["stats"]["possession"])
            else:
                away_possesion = json.dumps({})
                print("No value in away given.")
            if "touches" in match.doc["away"]["stats"]:
                away_touches = json.dumps(match.doc["away"]["stats"]["touches"])
            else:
                away_touches = json.dumps({})
                print("No value in away given.")
            if "passesTotal" in match.doc["away"]["stats"]:
                away_passes_total = json.dumps(match.doc["away"]["stats"]["passesTotal"])
            else:
                away_passes_total = json.dumps({})
                print("No value in away given.")
            if "passesAccurate" in match.doc["away"]["stats"]:
                away_passes_accurate = json.dumps(match.doc["away"]["stats"]["passesAccurate"])
            else:
                away_passes_accurate = json.dumps({})
                print("No value in away given.")
            if "passesKey" in match.doc["away"]["stats"]:
                away_passes_key = json.dumps(match.doc["away"]["stats"]["passesKey"])
            else:
                away_passes_key = json.dumps({})
                print("No value in away given.")
            if "passSuccess" in match.doc["away"]["stats"]:
                away_pass_success = json.dumps(match.doc["away"]["stats"]["passSuccess"])
            else:
                away_pass_success = json.dumps({})
                print("No value in away given.")
            if "aerialsTotal" in match.doc["away"]["stats"]:
                away_aerials_total = json.dumps(match.doc["away"]["stats"]["aerialsTotal"])
            else:
                away_aerials_total = json.dumps({})
                print("No value in away given.")
            if "aerialsWon" in match.doc["away"]["stats"]:
                away_aerials_won = json.dumps(match.doc["away"]["stats"]["aerialsWon"])
            else:
                away_aerials_won = json.dumps({})
                print("No value in away given.")
            if "aerialSuccess" in match.doc["away"]["stats"]:
                away_aerials_success = json.dumps(match.doc["away"]["stats"]["aerialSuccess"])
            else:
                away_aerials_success = json.dumps({})
                print("No value in away given.")
            if "offensiveAerials" in match.doc["away"]["stats"]:
                away_offensive_aerials = json.dumps(match.doc["away"]["stats"]["offensiveAerials"])
            else:
                away_offensive_aerials = json.dumps({})
                print("No value in away given.")
            if "defensiveAerials" in match.doc["away"]["stats"]:
                away_defensive_aerials = json.dumps(match.doc["away"]["stats"]["defensiveAerials"])
            else:
                away_defensive_aerials = json.dumps({})
                print("No value in away given.")
            if "cornersTotal" in match.doc["away"]["stats"]:
                away_corners_total = json.dumps(match.doc["away"]["stats"]["cornersTotal"])
            else:
                away_corners_total = json.dumps({})
                print("No value in away given.")
            if "throwInsTotal" in match.doc["away"]["stats"]:
                away_throw_ins_total = json.dumps(match.doc["away"]["stats"]["throwInsTotal"])
            else:
                away_throw_ins_total = json.dumps({})
                print("No value in away given.")
            if "throwInsAccurate" in match.doc["away"]["stats"]:
                away_throw_ins_accurate = json.dumps(match.doc["away"]["stats"]["throwInsAccurate"])
            else:
                away_throw_ins_accurate = json.dumps({})
                print("No value in away given.")
            if "foulsCommited" in match.doc["away"]["stats"]:
                away_fouls_commited = json.dumps(match.doc["away"]["stats"]["foulsCommited"])
            else:
                away_fouls_commited = json.dumps({})
                print("No value in away given.")
            if "tacklesTotal" in match.doc["away"]["stats"]:
                away_tackles_total = json.dumps(match.doc["away"]["stats"]["tacklesTotal"])
            else:
                away_tackles_total = json.dumps({})
                print("No value in away given.")
            if "tackleSuccessful" in match.doc["away"]["stats"]:
                away_tackles_successful = json.dumps(match.doc["away"]["stats"]["tackleSuccessful"])
            else:
                away_tackles_successful = json.dumps({})
                print("No value in away given.")
            if "tackleUnsuccesful" in match.doc["away"]["stats"]:
                away_tackles_unsuccessful = json.dumps(match.doc["away"]["stats"]["tackleUnsuccesful"])
            else:
                away_tackles_unsuccessful = json.dumps({})
                print("No value in away given.")
            if "tackleSuccess" in match.doc["away"]["stats"]:
                away_tackles_success = json.dumps(match.doc["away"]["stats"]["tackleSuccess"])
            else:
                away_tackles_success = json.dumps({})
                print("No value in away given.")
            if "dribbledPast" in match.doc["away"]["stats"]:
                away_dribbled_past = json.dumps(match.doc["away"]["stats"]["dribbledPast"])
            else:
                away_dribbled_past = json.dumps({})
                print("No value in away given.")
            if "dribblesWon" in match.doc["away"]["stats"]:
                away_dribbles_won = json.dumps(match.doc["away"]["stats"]["dribblesWon"])
            else:
                away_dribbles_won = json.dumps({})
                print("No value in away given.")
            if "dribblesAttempted" in match.doc["away"]["stats"]:
                away_dribbles_attempted = json.dumps(match.doc["away"]["stats"]["dribblesAttempted"])
            else:
                away_dribbles_attempted = json.dumps({})
                print("No value in away given.")
            if "dribblesLost" in match.doc["away"]["stats"]:
                away_dribbles_lost = json.dumps(match.doc["away"]["stats"]["dribblesLost"])
            else:
                away_dribbles_lost = json.dumps({})
                print("No value in away given.")
            if "dribbleSuccess" in match.doc["away"]["stats"]:
                away_dribble_success = json.dumps(match.doc["away"]["stats"]["dribbleSuccess"])
            else:
                away_dribble_success = json.dumps({})
                print("No value in away given.")
            if "dispossessed" in match.doc["away"]["stats"]:
                away_dispossessed = json.dumps(match.doc["away"]["stats"]["dispossessed"])
            else:
                away_dispossessed = json.dumps({})
                print("No value in away given.")
        else:
            print("No stats in away.")
    else:
        print("No away value given.")

    # Match Report hinzufügen
    match_report = MatchReport(website="whoscored.com", match_id=match_game.id,
                               # Home Attributes
                               home_scores=home_scores,
                               home_scores_ht=home_scores_halftime,
                               home_average_age=home_average_age,
                               home_ratings=home_ratings,
                               home_shots_total=home_shots_total,
                               home_shots_on_target=home_shots_on_target,
                               home_shots_off_target=home_shots_off_target,
                               home_shots_blocked=home_shots_blocked,
                               home_clearances=home_clearances,
                               home_interceptions=home_interceptions,
                               home_possesion=home_possesion,
                               home_touches=home_touches,
                               home_passes_total=home_passes_total,
                               home_passes_accurate=home_passes_accurate,
                               home_passes_key=home_passes_key,
                               home_pass_success=home_pass_success,
                               home_aerials_total=home_aerials_total,
                               home_aerials_won=home_aerials_won,
                               home_aerials_success=home_aerials_success,
                               home_offensive_aerials=home_offensive_aerials,
                               home_defensive_aerials=home_defensive_aerials,
                               home_corners_total=home_corners_total,
                               home_throw_ins_total=home_throw_ins_total,
                               home_throw_ins_accurate=home_throw_ins_accurate,
                               home_fouls_commited=home_fouls_commited,
                               home_tackles_total=home_tackles_total,
                               home_tackles_successful=home_tackles_successful,
                               home_tackles_unsuccessful=home_tackles_unsuccessful,
                               home_tackles_success=home_tackles_success,
                               home_dribbled_past=home_dribbled_past,
                               home_dribbles_won=home_dribbles_won,
                               home_dribbles_attempted=home_dribbles_attempted,
                               home_dribbles_lost=home_dribbles_lost,
                               home_dribble_success=home_dribble_success,
                               home_dispossessed=home_dispossessed,
                               # Away Attributes
                               away_scores=away_scores,
                               away_scores_ht=away_scores_halftime,
                               away_average_age=away_average_age,
                               away_ratings=away_ratings,
                               away_shots_total=away_shots_total,
                               away_shots_on_target=away_shots_on_target,
                               away_shots_off_target=away_shots_off_target,
                               away_shots_blocked=away_shots_blocked,
                               away_clearances=away_clearances,
                               away_interceptions=away_interceptions,
                               away_possesion=away_possesion,
                               away_touches=away_touches,
                               away_passes_total=away_passes_total,
                               away_passes_accurate=away_passes_accurate,
                               away_passes_key=away_passes_key,
                               away_pass_success=away_pass_success,
                               away_aerials_total=away_aerials_total,
                               away_aerials_won=away_aerials_won,
                               away_aerials_success=away_aerials_success,
                               away_offensive_aerials=away_offensive_aerials,
                               away_defensive_aerials=away_defensive_aerials,
                               away_corners_total=away_corners_total,
                               away_throw_ins_total=away_throw_ins_total,
                               away_throw_ins_accurate=away_throw_ins_accurate,
                               away_fouls_commited=away_fouls_commited,
                               away_tackles_total=away_tackles_total,
                               away_tackles_successful=away_tackles_successful,
                               away_tackles_unsuccessful=away_tackles_unsuccessful,
                               away_tackles_success=away_tackles_success,
                               away_dribbled_past=away_dribbled_past,
                               away_dribbles_won=away_dribbles_won,
                               away_dribbles_attempted=away_dribbles_attempted,
                               away_dribbles_lost=away_dribbles_lost,
                               away_dribble_success=away_dribble_success,
                               away_dispossessed=away_dispossessed)
    session_add(match_report)
    session_commit()

    # Beziehung hinzufügen
    asso = MatchReportAss(event_id=event.id, match_report_id=match_report.id)
    session_add(asso)
    session_commit()


def add_referee(match):
    if "referee" in match.doc:
        if "officialId" in match.doc["referee"]:
            referee_id = match.doc["referee"]["officialId"]
        else:
            print("No officialId given.")
        if "firstName" in match.doc["referee"]:
            referee_first_name = match.doc["referee"]["firstName"]
        else:
            referee_first_name = json.dumps({})
            print("No firstName in referee given.")
        if "lastName" in match.doc["referee"]:
            referee_last_name = match.doc["referee"]["lastName"]
        else:
            referee_last_name = json.dumps({})
            print("No lastName in referee given.")
        if not check_referee(referee_id):
            referee = Referee(id=referee_id, first_name=referee_first_name, last_name=referee_last_name)
            session_add(referee)
            session_commit()
    else:
        print("No referee given.")