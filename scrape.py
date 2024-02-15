import requests
from bs4 import BeautifulSoup
import json 
import jmespath
import datetime
import csv

def getData():
    for x in range (2002, datetime.date.today().year - 1):
        result = f"{x}-{x+1}|"
        URL= f"https://www.voetbalkrant.com/belgie/jupiler-pro-league/geschiedenis/{x}-{x+1}/wedstrijden"
        page= requests.get(URL)
        soup= BeautifulSoup(page.content, "html.parser")
        result = soup.table.get_text("|", strip=True)
        prepareData(result, x)
    print("Done")

def prepareData(data, jaar):
        data = data.split("|")
        speeldag = "0"
        datum = "00/00"
        tijd= ""
        huisploeg = ""
        wegploeg = ""
        stand = ""
        while (len(data) > 0):
             if "Speeldag" in data[0]:
                  speeldag = data[0][len(data[0]) -2:].strip()
                  data.pop(0)
             if "Testmatch" in data[0]:
                  speeldag = "Test"
                  data.pop(0)
             if "Supercup" in data[0]:
                  speeldag = "Supercup"
                  data.pop(0)
             if "Europa" in data[0]:
                  speeldag = "Play-Offs"
                  data.pop(0)
             if "Eindronde" in data[0]:
                  speeldag = "Eindronde"
                  data.pop(0)
             if "Vriend" in data[0]:
                  speeldag = "Vriend"
                  data.pop(0)
             if int(data[0][3])*10 + int(data[0][4]) > 7:
                  datum = data[0][:5] + f'/{jaar}'
             else:
                  datum = data[0][:5] + f'/{jaar + 1}'
             tijd = data[0][5:].strip()
             data.pop(0)
             huisploeg = data.pop(0)
             wegploeg = data.pop(0)
             stand = data.pop(0)
             writeData(datum, tijd, speeldag, huisploeg, wegploeg, stand)
             
        

            
                  

def writeData(datum, tijd, speeldag, huisploeg, wegploeg, stand):
    with open('data.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([datum, tijd, speeldag, huisploeg, wegploeg, stand])



getData()
        
