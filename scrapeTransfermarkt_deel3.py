# Deel 3

import requests
from bs4 import BeautifulSoup
import json
import jmespath
import datetime
import csv
import re

# Tijdstip

soup = ""
URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltag/wettbewerb/BE1/saison_id/2019/spieltag/13"
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
page= requests.get(URL, headers=headers)
soup= BeautifulSoup(page.content, "html.parser")
table = soup.select("#main main, div.row div.box:nth-of-type(1) div.content div.row tbody tr td:nth-of-type(2) div.inline-select div.chzn-container a.chzn-single span")

data = ""
for row in table:
  data += row.get_text("|", strip=True)
data = data.split("|")

for i in range(0, 28):
  data.pop(0)
     
seizoenen = [0] * 64

for i in range(0, 64):
  seizoenen[i] = data.pop(0)

data.pop(0)
     
speeldagen = [0] * 34

for i in range(0, 34):
  speeldagen[i] = data.pop(0)

def getData():
    for year in range (2022, datetime.date.today().year - 1):
        seizoen = seizoenen.pop()
        for day in range (1, 3):
          speeldag = speeldagen[day-1]
          URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltag/wettbewerb/BE1/saison_id/2019/spieltag/13"
          headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
          page= requests.get(URL, headers=headers)
          soup= BeautifulSoup(page.content, "html.parser")
          prepareData(soup, seizoen, speeldag)
          # print(soup)
    print("Done")


def writeData(seizoen, speeldag, datum, tijd, afkortingHuisploeg, huisploeg, stand, afkortingUitploeg, uitploeg):
    with open('data.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([seizoen, speeldag, datum, tijd, afkortingHuisploeg, huisploeg, stand, afkortingUitploeg, uitploeg])

def prepareData(soup, seizoen, speeldag):

     months = ["sep", "okt", "nov", "dec", "jan", "feb", "ma", "apr", "mei", "jun", "jul", "aug"]

     idstext = soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr td span a[title='Wedstrijdverslag']")
     href = idstext[0]['href']
     match = re.search(r'/spielbericht/index/spielbericht/(\d+)', href)
     if match:
      match_id = match.group(1)

     datum = ""
     tijd= ""
     afkortingHuisploeg = ""
     huisploeg = ""
     standThuisploeg = ""
     standUitploeg = ""
     afkortingUitploeg = ""
     uitploeg = ""
     stand = ""
     jaar= ""
     speeldag= ""
     scorendePloeg= ""
     tijdstipDoelpunt= ""

     table = soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr")

     data = ""
     for row in table:
          data += row.get_text("|", strip=True)
     data = data.split("|")
     for x in data:
          if "." in x and "(" in x:
               data.remove(x)

     for x in range(0, len(data)-1):
        if x >= len(data):
          break
        if re.match("[0-9]{2}:[0-9]{2}..", data[x]):
          data.remove(data[x])

     for x in range(0, len(data)-1):
        if x >= len(data)-1:
          break
        if data[x] == data[x+1]:
          data.remove(data[x])    

     new_data = []
     for x in data:
      new_data.extend(re.split(r"([0-9]+:[0-9]+)", x))
     data = new_data

     for x in range(0, len(data)-1):
      if x >= len(data)-1:
          break
      if data[x].startswith('-'):
        del data[x]
      
     for x in range(0, len(data)-1):
      if x >= len(data)-1:
          break
      if 'uur' in data[x]:
        del data[x]
      
     for x in range(0, len(data)-1):
      if x >= len(data)-1:
          break
      if len(data[x]) <= 2:
        del data[x]
      
     for x in range(0, len(data)-1):
      if x >= len(data)-1:
          break
      if 'Spelverloop' in data[x]:
        del data[x]
      
     for x in range(0, len(data)-1):
      if x >= len(data)-1:
          break
      if '%' in data[x]:
        del data[x]
      
    #  print(data)

     while len(data) > 0:
            item = data.pop(0)
            if any(month in item for month in months):
                datum = item.strip()
            if re.match(r"\d{2}:\d{2}", item):
                tijd = item.strip()
            if 'uur' in item:
                match = re.search(r"\d{2}:\d{2}", item)
                if match:
                    tijd = match.group()
            if re.search(r"saison_id/(\d{4})", URL):
              jaar = re.search(r"saison_id/(\d{4})", URL).group(1)
            if re.search(r"spieltag/(\d+)", URL):
              speeldag = re.search(r"spieltag/(\d+)", URL).group(1)

            if ":" in item:
              for d in data:
                if "'" in d:
                    tijdstipDoelpunt = d
                    data.remove(d)
              if data and data[0].isdigit():
                scorendePloeg = uitploeg
              else:
                scorendePloeg = huisploeg


    #  print(f"Jaar: ", jaar)
    #  print(f"Speeldag: ", speeldag)
    #  print(f"datum: ", datum)
    #  print(f"tijd: ", tijd)
    #  print(f"scorendePloeg: ", scorendePloeg)
    #  print(f"tijdstipDoelpunt: ", tijdstipDoelpunt)
    #  print(f"standThuisploeg: ", standThuisploeg)
    #  print(f"standUitploeg: ", standUitploeg)
    


getData()