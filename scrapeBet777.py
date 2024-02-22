import requests
from bs4 import BeautifulSoup
import json 
import jmespath
import datetime
import csv

def getData():
    # Gebruik API om momentele "odds" te krijgen
    URL= "https://api.sportify.bet/echo/v1/events?sport=voetbal&competition=belgium-first-division-a&key=market_type&lang=nl&bookmaker=bet777"
    page= requests.get(URL)
    soup= BeautifulSoup(page.content, "lxml")
    result = soup.find('p').text
    # Maakt JSON object aan 
    json_object = json.loads(result)
    prepareData(json_object)

def prepareData(json_object):
        oddsWinnaar1 = 0
        oddsWinnaarX = 0
        oddsWinnaar2 = 0
        totaalgoalsplus = 0
        totaalgoalsmin = 0 
        beideteams = 0
        beideteamsniet = 0
        count = len(jmespath.search(f'tree[0].competitions[0].events', json_object))
        for x in range(0, count):
            huisploeg = jmespath.search(f'tree[0].competitions[0].events[{x}].home_team', json_object)
            wegploeg = jmespath.search(f'tree[0].competitions[0].events[{x}].away_team', json_object)
            for y in range(0,3):
                outcomes = jmespath.search(f'tree[0].competitions[0].events[{x}].markets[{y}].outcome_count', json_object)
                for z in range (0, outcomes):
                    odds = str((jmespath.search(f'tree[0].competitions[0].events[{x}].markets[{y}].outcomes[{z}].odds', json_object)))
                    match str((jmespath.search(f'tree[0].competitions[0].events[{x}].markets[{y}].outcomes[{z}].name', json_object))):
                        case "Ja":
                            beideteams = odds
                        case "Nee":
                            beideteamsniet = odds
                        case "1":
                            oddsWinnaar1 = odds
                        case "2":
                            oddsWinnaar2 = odds
                        case "Gelijkspel":
                            oddsWinnaarX = odds
                        case "Meer dan (2.5)":
                            totaalgoalsplus = odds
                        case ("Onder (2.5)"):
                            totaalgoalsmin = odds
                        case _:
                            print("Woopsie")
            writeData(huisploeg, wegploeg, oddsWinnaar1, oddsWinnaarX, oddsWinnaar2, totaalgoalsplus, totaalgoalsmin, beideteams, beideteamsniet)


def writeData(huisploeg, wegploeg, oddsWinnaar1, oddsWinnaarX, oddsWinnaar2, totaalgoalsplus, totaalgoalsmin, beideteams, beideteamsniet):
    with open('dataBet777.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([huisploeg, wegploeg, oddsWinnaar1, oddsWinnaarX, oddsWinnaar2, totaalgoalsplus, totaalgoalsmin, beideteams, beideteamsniet])


def clearData():
    with open('dataBet777.csv', 'w', newline='') as file:
        file.close()


clearData()
getData()
        
