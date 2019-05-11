from model.db import get_sorted_matches, session_add, session_commit
import math
import operator
import json

from model.table import Table


def compute_table(season_id):
    matches = get_sorted_matches(season_id)
    teams = set()
    for match in matches:
        # alle teams
        teams.add(match.home_team)
        teams.add(match.away_team)

    table = {}
    for team in list(teams):
        table[team] = {"position": 1,
                       "match_day": 0,
                       "wins": 0,
                       "loses": 0,
                       "equals": 0,
                       "goals": 0,
                       "againstgoals": 0,
                       "goaldifference": 0,
                       "points": 0}
    # spieltag
    index = math.floor(len(list(teams)) / 2)
    match_day = 0
    tmp_date = 0
    for match in matches:
        index = index + 1
        tmp_date = match.date
        if index >= math.floor(len(list(teams)) / 2):
            index = 0
            # add after match day
            table_sql = Table(date=match.date, table=json.dumps(table), match_day=match_day, season_id=season_id)
            session_add(table_sql)
            session_commit()

            match_day = match_day + 1

            # get home team goasl
        home_team = match.home_team
        home_team_goals = int(match.score.replace(' ', '').split(':')[0])
        # get away team goals
        away_team = match.away_team
        away_team_goals = int(match.score.replace(' ', '').split(':')[-1])
        # add goals and awaygoals to the table
        table[home_team]["goals"] = table[home_team]["goals"] + home_team_goals
        table[home_team]["againstgoals"] = table[home_team]["againstgoals"] + away_team_goals
        table[home_team]["goaldifference"] = table[home_team]["goals"] - table[home_team]["againstgoals"]
        # add goals and awaygoals to the table
        table[away_team]["goals"] = table[away_team]["goals"] + away_team_goals
        table[away_team]["againstgoals"] = table[away_team]["againstgoals"] + home_team_goals
        table[away_team]["goaldifference"] = table[away_team]["goals"] - table[away_team]["againstgoals"]

        if home_team_goals > away_team_goals:
            table[home_team]["wins"] = table[home_team]["wins"] + 1
            table[home_team]["points"] = table[home_team]["points"] + 3
            table[away_team]["loses"] = table[away_team]["loses"] + 1
        elif home_team_goals == away_team_goals:
            table[home_team]["equals"] = table[home_team]["equals"] + 1
            table[home_team]["points"] = table[home_team]["points"] + 1
            table[away_team]["equals"] = table[away_team]["equals"] + 1
            table[away_team]["points"] = table[away_team]["points"] + 1
        else:
            table[away_team]["wins"] = table[away_team]["wins"] + 1
            table[away_team]["points"] = table[away_team]["points"] + 3
            table[home_team]["loses"] = table[home_team]["loses"] + 1

        # match day
        table[home_team]["match_day"] = match_day
        table[away_team]["match_day"] = match_day

        # update the table
        # sort by point and goal difference
        tmp_list = []
        for elem in table.items():
            tmp = [elem[0], elem[1]['points'], elem[1]['goaldifference']]
            tmp_list.append(tmp)
        # sort by points and goaldifference
        tmp_list = sorted(tmp_list, key=operator.itemgetter(1, 2))[::-1]
        # change table positions
        for idx, val in enumerate(tmp_list):
            table[val[0]]["position"] = idx + 1

    # add after match day
    table_sql = Table(date=tmp_date, table=json.dumps(table), match_day=match_day, season_id=season_id)
    session_add(table_sql)
    session_commit()
