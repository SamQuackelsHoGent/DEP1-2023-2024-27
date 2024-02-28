# Deel 1

import requests
from bs4 import BeautifulSoup
import json
import jmespath
import datetime
import csv
import re

# Seizoenen en speeldagen

# soup = ""
# URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltagtabelle/wettbewerb/BE1?saison_id=1960&spieltag=1"
# headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
# page= requests.get(URL, headers=headers)
# soup= BeautifulSoup(page.content, "html.parser")
# table = soup.select("#main main, div.row div.box:nth-of-type(1) div.content div.row tbody tr td:nth-of-type(2) div.inline-select div.chzn-container a.chzn-single span")

# data = ""
# for row in table:
#   data += row.get_text("|", strip=True)
# data = data.split("|")

# for i in range(0, 28):
#   data.pop(0)
     
# seizoenen = [0] * 64

# for i in range(0, 64):
#   seizoenen[i] = data.pop(0)

# data.pop(0)
     
# speeldagen = [0] * 34

# for i in range(0, 34):
#   speeldag = data.pop(0)
#   if (re.match("^[0-9].*", speeldag)):
#     speeldagen[i] = re.findall(r'\d+', speeldag)

# print(speeldagen)

def getData():
    for year in range (1960, datetime.date.today().year - 1):
        seizoen = (str(year)[2:] + "/" + str(year + 1)[2:])
        for day in range (1, 35):
          speeldag = day
          URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltagtabelle/wettbewerb/BE1?saison_id={year}&spieltag={day}"
          headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
          page= requests.get(URL, headers=headers)
          soup= BeautifulSoup(page.content, "html.parser")
          prepareData(soup, seizoen, speeldag)
    print("Done")

def writeData(seizoen, speeldag, datum, tijd, afkortingHuisploeg, huisploeg, huisstand, uitstand, afkortingUitploeg, uitploeg):
    #with open('test.csv', 'a', newline='\n') as file:
    with open('dataTransfermarktDeel1.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([seizoen, speeldag, datum, tijd, afkortingHuisploeg, huisploeg, huisstand, uitstand, afkortingUitploeg, uitploeg])




def prepareData(soup, seizoen, speeldag):
  global datum, tijd, afkortingHuisploeg, huisploeg, standThuisploeg, standUitploeg, afkortingUitploeg, uitploeg, stand
  datum = ""
  tijd= ""
  afkortingHuisploeg = ""
  huisploeg = ""
  standThuisploeg = ""
  standUitploeg = ""
  afkortingUitploeg = ""
  uitploeg = ""
  stand = ""
  months = ["sep", "okt", "nov", "dec", "jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug"]
  table = soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr")

  data = ""
  for row in table:
      data += row.get_text("|", strip=True)
  data = data.split("|")
  for x in data:
      if "." in x and "(" in x:
            data.remove(x)

  x = 0
  while (x < len(data)-1):
    if x >= len(data):
      pass
    elif len(data[x]) <= 2:
        data.remove(data[x])
        x -= 1
    elif re.match("[0-9]{2}:[0-9]{2}..", data[x]):
      data.remove(data[x])
      x -= 1
    elif x < len(data)-1:
      if data[x] == data[x+1] or data[x] == data[x-1]:
        data.remove(data[x])
        x -= 1
    x += 1


  while (len(data) > 0):
    if any(month in data[0] for month in months):
        datum = data.pop(0)
    if re.match("[0-9]{2}:[0-9]{2}", data[0]):
      tijd = data.pop(0)
    afkortingHuisploeg = data.pop(0)
    if afkortingHuisploeg == "Standard Luik":
      huisploeg = "Standard Luik"
    elif afkortingHuisploeg == "Germinal Ekeren":
       huisploeg = "Germinal Ekeren"
    else:
      huisploeg = data.pop(0)
    stand = data.pop(0)
    if stand != "verplaatst":
      huisstand = stand.split(":")[0]
      uitstand = stand.split(":")[1]
    else:
      huisstand = 0
      uitstand = 0
    afkortingUitploeg = data.pop(0)
    if afkortingUitploeg == "Standard Luik":
      uitploeg = "Standard Luik"
    elif afkortingUitploeg == "Germinal Ekeren":
       uitploeg = "Germinal Ekeren"
    else:
      uitploeg = data.pop(0)

    if datum == "" or tijd == "" or speeldag == "" or seizoen == "":
       print("Fuck")
       print(seizoen, speeldag, datum, tijd, afkortingHuisploeg, huisploeg, huisstand, uitstand, afkortingUitploeg, uitploeg)
       quit

    for x in range(0, len(data)-1):
        if x >= len(data)-1:
          break
        if data[x] == data[x+1]:
          data.remove(data[x])

    while (len(data) > 0):
          if len(data) < 1:
            break
          if any(month in data[0] for month in months):
               datum = data.pop(0)
          if len(data) < 1:
            break
          if re.match("[0-9][0-9]:[0-9][0-9]", data[0]):
            tijd = data.pop(0)
          if len(data) < 1:
            break
          afkortingHuisploeg = data.pop(0)
          if len(data) < 1:
            break
          if afkortingHuisploeg == "Standard Luik":
            huisploeg = "Standard Luik"
          else:
            huisploeg = data.pop(0)
          if len(data) < 1:
            break
          stand = data.pop(0)
          if len(data) < 1:
            break
          afkortingUitploeg = data.pop(0)
          if len(data) < 1:
            break
          if afkortingUitploeg == "Standard Luik":
            uitploeg = "Standard Luik"
          else:
            uitploeg = data.pop(0)

          writeData(seizoen, speeldag, datum, tijd, afkortingHuisploeg, huisploeg, huisstand, uitstand, afkortingUitploeg, uitploeg)


getData()