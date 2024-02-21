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
    result = soup.find("p").text
    # Maakt JSON object aan 
    json_object = json.loads(result)
    data = jmespath.search("tree", json_object)
    print(json_object)
    
    print("Done")

def prepareData(data, jaar):
        data = data.split("|")
        writeData()
            
                  

def writeData():
    with open('dataBet777.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([])



getData()
        
