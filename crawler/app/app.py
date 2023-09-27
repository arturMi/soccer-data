from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from crawler import *
# import os
import csv
import sys

from config import *

if __name__ == "__main__":
    # parse_bl_wp()
    print('NOTHING SPECIAL HERE ')


def loaod_from_csv():
    """
        Load data from the avaiable csv files with basic information for every game until BL 17/18

        :param none
    """
    # Create a scoped session
    session = create_session()
    # my code here

    teams = session.query(Team).all()

    seasons = session.query(Season).all()

    matches = []

    f = open('data/2-buli-16-ii.csv', 'rt')
    try:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            matches.append({
                'date': row[0],
                'season_year': row[1],
                'gameday': row[2],
                'home': row[3],
                'visitor': row[4],
                'h_goal': row[5],
                'v_goal': row[6],
            })
            # print(row)
    finally:
        f.close()

    for match in matches:
        # search for home team id
        for team in teams:
            if team.name == match['home']:
                match['home_id'] = team.id
            if team.name == match['visitor']:
                match['visitor_id'] = team.id

        # search for the season id
        for season in seasons:
            if str(season.year) == match['season_year'] and season.league_id == 1:
                match['season_id'] = season.id
                break
        # add to db
        session.add(Match(season_id=match['season_id'], matchday=match['gameday'], hometeamid=match['home_id'],
                          awayteamid=match['visitor_id'],
                          date=match['date'], hometeamname=match['home'], awayteamname=match['visitor'],
                          hometeamgoals=match['h_goal'], awayteamgoals=match['v_goal']))
    # print(matches)
    #
    # f = open('germany2.csv', 'rt')
    # try:
    #     reader = csv.reader(f)
    #     next(reader)
    #     for row in reader:
    #         teams.add(row[2])
    #         teams.add(row[3])
    # finally:
    #     f.close()
    #
    # for team in teams:
    #     session.add(Team(name=team))
    #
    #
    # print(teams)

    # for i in range(1963, 2018):
    #     season_title = 'Bundesliga ' + str(i) + '/' + str(i + 1)[-2:]
    #     session.add(Season(1, title=season_title, year=i))

    session.commit()
    #
    # # remove the session
    session.remove()


def create_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = scoped_session(sessionmaker())
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return session
