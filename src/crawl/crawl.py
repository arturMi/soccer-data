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
from model.db import save_game_to_database

# Webseite
base_url = "https://www.whoscored.com"
# header damit die Webseite denkt dass mit Browser auf die Seite zugegriffen wird
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)


# Url
def get_game_data(url):
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
    #print(main)

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
