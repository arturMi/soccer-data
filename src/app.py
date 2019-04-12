from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from crawl import *
# import os
import sys

from config import *

def load_from_json():
    '''
        Load the data of the matches from the json file
    '''

    # Create a scoped session
    session = create_session()

    # Öffnet Text Datei
    match_data = open('game_result.txt', 'rt')

    # Datei öffnen und in JSON-File formatieren
    g = open('data.json', 'rt')
    loaded_json = json.loads(g)

    for x in loaded_json:
        print("%s: %d" % (x, loaded_json[x]))


def create_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = scoped_session(sessionmaker())
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return session