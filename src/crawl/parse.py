from model.db import get_match_data

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
        # # Unique Team-ID
        # match.doc["home"]["teamId"]
        # # Team Name
        # match.doc["home"]["name"]
        # # Land des Teams
        # match.doc["home"]["countryName"]
        # # Manager des Teams
        # match.doc["home"]["managerName"]
        # # Durchschnittsalter Heim
        # match.doc["home"]["averageAge"]
        # #Spieler Heim-Team
        for player in match.doc["home"]["players"]:
        #     # Unique Player-ID
        #     player["playerId"]
        #     # Name
        #     player["name"]
        #     # Größe
        #     player["height"]
        #     # Gewicht
        #     player["weight"]
        #     # Alter
        #     player["age"]
        #     # Startelf boolean
        #     player["isFirstEleven"]
        #     # Man of the Match boolean
        #     player["isManOfTheMatch"]
        #
            if "totalSaves" in player["stats"]:
                print(player["stats"]["totalSaves"])
        #
        # #Auswärts-Team
        # # Unique Team-ID
        # match.doc["away"]["teamId"]
        # # Team Name
        # match.doc["away"]["name"]
        # # Land des Teams
        # match.doc["away"]["countryName"]
        # # Manager des Teams
        # match.doc["away"]["managerName"]
        # # Durchschnittsalter Auswärts
        # match.doc["away"]["averageAge"]
        # # Spieler Auswärts-Team
        # for player in match.doc["away"]["players"]:
        #     player["playerId"]
        #     # Name
        #     player["name"]
        #     # Größe
        #     player["height"]
        #     # Gewicht
        #     player["weight"]
        #     # Alter
        #     player["age"]
        #     # Startelf boolean
        #     player["isFirstEleven"]
        #     # Man of the Match boolean
        #     player["isManOfTheMatch"]
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