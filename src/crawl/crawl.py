# Regex - to replace and find string
import re
# String to list dicts
import ast
# json parser
import json
# Html get requests
import requests
# HTML parser
from bs4 import BeautifulSoup
from random import randint
from time import sleep

from model.db import save_game_to_database, get_match_day_data, session_commit

# Webseite
base_url = "https://www.whoscored.com"
# header damit die Webseite denkt dass mit Browser auf die Seite zugegriffen wird
headers = requests.utils.default_headers()
headers.update(
    {
    'Host': 'www.whoscored.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.whoscored.com/Regions/81/Tournaments/3/Seasons/6902/Germany-Bundesliga',
    'Model-last-Mode': '+ZMeVfn+cESNj4xd94TzoAVlHQZXDuZ+DF8FAYoxfUY=',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Cookie': 'visid_incap_774904=cSykh4WqRVmBCfw5/R71wW7dWVwAAAAAQUIPAAAAAABFrMVOc+joVXbYNuv+X/fX; permutive-session=%7B%22session_id%22%3A%2201b3b698-9869-4c11-8827-e570478713fb%22%2C%22last_updated%22%3A%222019-04-03T08%3A09%3A29.060Z%22%7D; permutive-id=d88cdd1f-b90a-4a39-8db8-90601d1bd3d3; _ga=GA1.2.699282445.1549393231; _pdfps=%5B%5D; cto_lwid=442a3883-66c4-442e-a861-98fe67b15667; cto_idcpy=e180b395-c669-4246-b398-05f183b45f0f; __gads=ID=2367a711f0f5979e:T=1549393270:S=ALNI_MaymRZ5xBCY3jtPwYS3HaF0shB1Gg; vg=fb97c37f-96e3-405d-9fc8-be817c11c899; _ym_uid=15537002746350893; _ym_d=1553700274; vl=1:0.00|2:DE|3:BADEN-WURTTEMBERG|4:|5:BADEN-WURTTEMBERG/|6:BADEN-WURTTEMBERG/ALBER|7:89073|!0; vd=hs-ulm.de; _pubcid=f64d8af6-bd3e-4b4a-95ea-828ebdd1640e; incap_ses_867_774904=wvjAVePyxBOqWngAoDQIDFe3sFwAAAAAjKMofgdhqOlPOeLnr30+5w==',
    'TE': 'Trailers'
    }
)


# Url
def get_game_data(url):
    """
        Get game data
    """
    search_url = base_url + url

    # Struktur in der URL finden, alle URL der Spiele crawlen

    # Get HTTPS request
    response = requests.get((search_url), headers=headers)
    # Parse html website
    html = BeautifulSoup(response.text, "html.parser")

    # print(html)
    # find div layout content wrapper - da sind die ganzen wichtigen daten drin
    # prettify - fügt Zeilensprünge ein
    main = html.find(id='layout-content-wrapper').prettify()
    # print(main)

    # Speichern die Main als Text File
    # Weil ansonsten nach 5 - 10 requests wird IP geblockt
    # Speichern die HTML als lokale File ab
    with open("tmp.txt", "w") as f:
        f.write(str(main.encode('ascii', 'ignore').decode('ascii')))

    ## REGEX
    # Finde Zeile mit substring matchHeader.load([
    match_header = re.compile(r'matchHeader.load\(\[')

    # Finde Zeile mit substring matchCentreData
    match_centre = re.compile(r'matchCentreData')

    # Öffne text file was ich gespeichert habe
    # itereiere jeden Zeilensprung
    # line ist eine Linie im Text file
    with open('tmp.txt', 'r', encoding='ascii') as file:
        for line in file:

            # Wenn die Zeile mit substring matchHeader.load([
            if match_header.search(line):
                # Regex und holen alles zwischen "[X...]"
                # Alles was zwischen den Eckigen Klammern ist
                match_header_str = re.findall('\[.*?\]', line)[0]

                # Jede stelle mit zwei Kommas hinter einander ersetzen durch ein Komma
                match_header_str_wc = match_header_str.replace(',,', '')

                # Text linie zu python list
                # match_header_list = ast.literal_eval(match_header_str_wc)
                # print(match_header_str_wc)

            # Wenn die Zeile mit substring matchCentreData
            if match_centre.search(line):
                print(line)
                #  wir holen die linie mit dem substring matchCentreData
                # holen und alle characters zwischen '= ... ;'
                match_centre_str = re.findall('=.*?;', line)[0]

                # Lösche "= " aus dem String
                match_centre_str = match_centre_str.replace('= ', '')
                # Lösche ; aus dem string
                match_centre_str = match_centre_str.replace(';', '')

                # Sting to JSON - pyhton dict
                match_centre_dict = json.loads(match_centre_str)
                # print(match_centre_dict)

    save_game_to_database(match_header_str_wc, match_centre_dict)


def crawl_match_day_data(season):
    """
        Get raw match day data
    """
    # get seasons
    seasons = get_match_day_data(season)
    # iterate over seasons
    for match_day in seasons:
        print(match_day.match_day_url)
        # get query
        response = requests.get((match_day.match_day_url), headers=headers)
        # response text
        match_day.data = response.text
        # Sleep between 5 and 50 seconds
        sleep(randint(5, 50))
    session_commit()