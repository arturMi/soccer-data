from model.db import create_tables, get_match_day_data, generate_game_url, get_match_data
from crawl.crawl import get_game_data, crawl_match_day_data, crawl_match_data
from crawl.parse import parse_to_player, parse_to_match


if __name__ == "__main__":
    # create_tables()
    # get_game_data('/Matches/1294781/Live/Germany-Bundesliga-2018-2019-Mainz-05-Freiburg')
    # crawl_match_day_data("2017/2018")
    # generate_game_url("2017/2018")
    # crawl_match_data()
    parse_to_player()


