from random import randint
from time import sleep
import re
import datetime

import requests
from bs4 import BeautifulSoup

#from app import create_session


base_url = "https://www.transfermarkt.de"


def crawl_bl_info():
    """
        Get all avaiable Bundesliga match data

        :param none
    """
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    search_url = base_url + "/2-bundesliga/gesamtspielplan/wettbewerb/L2/saison_id/"

    for year in range(1981, 2017):
        # params = {'saison_id': year,
        #           'spieltagVon': 1,
        #           'spieltagBis': 50}
        response = requests.get((search_url + str(year)), headers=headers)
        html = BeautifulSoup(response.text, "html.parser")
        # get the main div
        main = html.find(id='main').prettify()
        with open(('./data/leauge-wp/BL2-' + str(year) + '.html'), 'w') as f:
            f.write(str(main.encode('ascii', 'ignore').decode('ascii')))
        sleep(randint(1, 4))


def parse_bl_wp():
    """
        Parse the crawled web pages in the database and check if the csv data was correct

        :param none
    """
    # database connection info
    session = create_session()
    # get all teams first of all
    teams = session.query(Team).all()
    # 1 for BL 1 and 2 for BL 2
    league_id = 2
    # get all teams with the right id
    # for year in range(1981, 2017):
    for year in range(1981, 2017):
        counter = 0
        with open('./data/leauge-wp/BL2-' + str(year) + '.html', 'r', encoding='ascii') as file:
            season = []
            soup = BeautifulSoup(file, 'html.parser')
            matchdays = soup.find_all('div', class_='large-6 columns')
            for matchday in matchdays:
                if matchday.find(class_='table-header'):
                    # extract the matchday e.g. Spieltag 1  -> 1
                    day = re.findall(r'\d+', matchday.find(class_='table-header').get_text())[0]
                    # parse the table
                    date = -1
                    time = -1
                    for tr in matchday.find("table").find('tbody').find_all('tr'):
                        # skip the emtpy table lines
                        if tr.find(class_='hide-for-small'):
                            # get the date
                            if tr.find(class_='hide-for-small').find('a').get_text().strip():
                                date = tr.find(class_='hide-for-small').find('a').get_text().strip()
                                # date = parser.parse(date).date()
                                date = datetime.datetime.strptime(date, '%d.%m.%Y')
                                time = tr.find(class_='zentriert hide-for-small').get_text().strip().split(':')
                                try:
                                    time = datetime.time(int(time[0]), int(time[1]), 0)
                                except:
                                    time = datetime.time(0, 0, 0)

                            # home team infromation
                            home_team = tr.find(class_='text-right no-border-rechts hauptlink').find(
                                'a').get_text().strip()
                            home_team_rank = tr.find(class_='text-right no-border-rechts hauptlink').find(
                                class_='tabellenplatz').get_text().strip()
                            home_team_rank = int(re.findall(r'\d+', home_team_rank)[0])
                            home_team_id = int(
                                tr.find(class_='text-right no-border-rechts hauptlink').find('a').get('id'))

                            # away team information
                            away_team = tr.find(class_='no-border-links hauptlink').find('a').get_text().strip()
                            away_team_rank = tr.find(class_='no-border-links hauptlink').find(
                                class_='tabellenplatz').get_text().strip()
                            away_team_rank = int(re.findall(r'\d+', away_team_rank)[0])
                            away_team_id = int(tr.find(class_='no-border-links hauptlink').find('a').get('id'))

                            # result
                            result = tr.find(class_='zentriert hauptlink').find('a').get_text().strip()
                            try:
                                home_goals = int(result.split(':')[0])
                                away_goals = int(result.split(':')[1])
                            except:
                                home_goals = -1
                                away_goals = -1

                            result_id = int(tr.find(class_='zentriert hauptlink').find('a').get('id'))

                            # get the db id of the teams
                            home_team_db_id = -1
                            away_team_db_id = -1
                            for team in teams:
                                if team.team_id == home_team_id:
                                    home_team_db_id = team.id
                                if team.team_id == away_team_id:
                                    away_team_db_id = team.id

                            season.append({
                                'gameday': day,
                                'date': date,
                                'time': time,
                                'match_id': result_id,

                                'home_team_name': home_team,
                                'away_team_name': away_team,

                                'home_goals': home_goals,
                                'away_goals': away_goals,

                                'home_id': home_team_id,
                                'home_db_id': home_team_db_id,
                                'home_rank': home_team_rank,

                                'away_id': away_team_id,
                                'away_db_id': away_team_db_id,
                                'away_rank': away_team_rank

                            })
                            counter += 1
                            # check against the data in the db and update wrong values and add information to it
            print('WP ' + str(counter))
            # print(season)
            # get season id of the specific year and league
            tmp_season = session.query(Season).filter_by(year=year, league_id=league_id).first()
            matchs = session.query(Match).filter_by(season_id=tmp_season.id)
            counter = 0
            # combine the two avaiable datasets and correct if not correct
            for match_crawled in season:
                # boolean to check if match is missing - if missing it will be added
                check = False
                for match in matchs:
                    if match.hometeamid == match_crawled['home_db_id'] and match.awayteamid == match_crawled[
                        'away_db_id']:
                        # and match.hometeamgoals == match_crawled['home_goals'] \
                        #     and match.awayteamgoals == match_crawled['away_goals']:

                        # correct the date
                        if not match.date == match_crawled['date']:
                            match.date = match_crawled['date']
                        # set all the other values
                        match.time = match_crawled['time']
                        match.match_id = match_crawled['match_id']
                        match.matchday = match_crawled['gameday']
                        match.hometeamrank = match_crawled['home_rank']
                        match.awayteamrank = match_crawled['away_rank']
                        counter += 1
                        check = True
                        break
                if not check:
                    # missing game add the game to the db
                    session.add(
                        Match(season_id=tmp_season.id,
                              hometeamid=match_crawled['home_db_id'],
                              awayteamid=match_crawled['away_db_id'],
                              date=match_crawled['date'],
                              time=match_crawled['time'],
                              matchday=match_crawled['gameday'],
                              hometeamname=match_crawled['home_team_name'],
                              awayteamname=match_crawled['away_team_name'],
                              hometeamgoals=match_crawled['home_goals'],
                              awayteamgoals=match_crawled['away_goals'],
                              match_id=match_crawled['match_id'],
                              hometeamrank=match_crawled['home_rank'],
                              awayteamrank=match_crawled['away_rank'],
                              )
                    )
                    print(match_crawled)
            print('DB ' + str(counter))
            # print(season)
        session.commit()
    # remove the session
    session.remove()
