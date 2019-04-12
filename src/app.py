from model.db import create_tables
from crawl.crawl import get_game_data


if __name__ == "__main__":
    #create_tables()
    get_game_data('/Matches/1294781/Live/Germany-Bundesliga-2018-2019-Mainz-05-Freiburg')