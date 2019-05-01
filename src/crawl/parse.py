from model.db import get_match_data, session_add, session_commit, check_league, check_team, check_trainer, get_trainer, \
    get_team
from model.season import Season
from model.league import League

from model.team import Team
from model.trainer import Trainer
from model.team_trainer_ass import TeamTrainerAss

from dateutil import parser


def parse():
    # add bundesliga if not already in there
    # add bundesliga
    l = "Bundesliga"
    c = 'Germany'
    y = 2017
    add_league_season(l, c, y)

    matches = get_match_data()
    for match in matches:
        # add match
        add_match(match)
        # add trainer team
        add_trainer_team(match)


def parse_to_match():
    matches = get_match_data()
    for match in matches:
        # Stadion
        match.doc["venueName"]
        # Spielbeginn(Datum,Uhrzeit)
        match.doc["startTime"]
        # Endergebnis
        match.doc["score"]
        # Halbzeitstand
        match.doc["htScore"]
        # Schiedsrichter
        match.doc["referee"]["name"]
        # Statistiken Heim
        for stats in match.doc["home"]["stats"]:
            stats["shotsBlocked"]

        # Statistiken Auswärts


def parse_to_player():
    matches = get_match_data()
    for match in matches:
        # Unique Team-ID
        match.doc["home"]["teamId"]
        # Team Name
        match.doc["home"]["name"]
        # Land des Teams
        match.doc["home"]["countryName"]
        # Manager des Teams
        match.doc["home"]["managerName"]
        # Durchschnittsalter Heim
        match.doc["home"]["averageAge"]
        # Spieler Heim-Team
        for player in match.doc["home"]["players"]:
            # Unique Player-ID
            player["playerId"]
            # Name
            player["name"]
            # Größe
            player["height"]
            # Gewicht
            player["weight"]
            # Alter
            player["age"]
            # Startelf boolean
            player["isFirstEleven"]
            # Man of the Match boolean
            player["isManOfTheMatch"]
            # Statistik
            if "totalSaves" in player["stats"]:
                player["stats"]["totalSaves"]

            if "collected" in player["stats"]:
                player["stats"]["collected"]

            if "claimsHigh" in player["stats"]:
                player["stats"]["claimsHigh"]

            if "posession" in player["stats"]:
                player["stats"]["possesion"]

            if "ratings" in player["stats"]:
                player["stats"]["ratings"]

            if "clearances" in player["stats"]:
                player["stats"]["clearances"]

            if "touches" in player["stats"]:
                player["stats"]["touches"]

            # Auswärts-Team
            # Unique Team-ID
            match.doc["away"]["teamId"]
            # Team Name
            match.doc["away"]["name"]
            # Land des Teams
            match.doc["away"]["countryName"]
            # Manager des Teams
            match.doc["away"]["managerName"]
            # Durchschnittsalter Auswärts
            match.doc["away"]["averageAge"]
            # Spieler Auswärts-Team
        for player in match.doc["away"]["players"]:
            # Spieler ID
            player["playerId"]
            # Name
            player["name"]
            # Größe
            player["height"]
            # Gewicht
            player["weight"]
            # Alter
            player["age"]
            # Startelf boolean
            player["isFirstEleven"]
            # Man of the Match boolean
            player["isManOfTheMatch"]


def add_league_season(name, country, year):
    if not check_league(name):
        bl = League(name=name, country=country)
        session_add(bl)
        session_commit()
        # add season to the league
        season = Season(league_id=bl.id, year=year)
        session_add(season)
        session_commit()


def add_match(match):
    print('ACAB')


def add_trainer_team(match):
    home_team_trainer = match.doc["home"]["managerName"]
    print(home_team_trainer)

    # add team
    home_team_id = match.doc["home"]["teamId"]
    home_team_name = match.doc["home"]["name"]

    # start time
    start_time = parser.parse(match.doc["startTime"])
    print(start_time)  #
    #
    # add trainer
    if not check_trainer(home_team_trainer):
        home_trainer = Trainer(name=home_team_trainer)
        session_add(home_trainer)
        session_commit()
    else:
        home_trainer = get_trainer(home_team_trainer)

    # add team
    if not check_team(home_team_id):
        home_team = Team(id=home_team_id, team_name=home_team_name)
        session_add(home_team)
        session_commit()
    else:
        home_team = get_team(home_team_id)

    # add relationship between
    print(home_team.id)
    print(home_trainer.id)
    asso = TeamTrainerAss(team_id=home_team.id, trainer_id=home_trainer.id, date=start_time)
    session_add(asso)
    session_commit()


'''
def parse_to_team():
    matches = get_match_data()
    for match in matches:


def parse_to_season():
    matches = get_match_data()
    for match in matches:


def parse_to_trainer():
    matches = get_match_data()
    for match in matches:


def parse_to_table():
    matches = get_match_data()
    for match in matches:
'''
