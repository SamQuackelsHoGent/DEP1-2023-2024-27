# Used imports
import requests
from bs4 import BeautifulSoup
import datetime
import csv
import re

# Code om de seizoenen en speeldagen te scrapen.

# Soup select om de seizoenen en speeldagen te selecteren
soup = ""
URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltagtabelle/wettbewerb/BE1?saison_id=1960&spieltag=1"
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
page= requests.get(URL, headers=headers)
soup= BeautifulSoup(page.content, "html.parser")
table = soup.select("#main main, div.row div.box:nth-of-type(1) div.content div.row tbody tr td:nth-of-type(2) div.inline-select div.chzn-container a.chzn-single span")

# Split de data
data = ""
for row in table:
  data += row.get_text("|", strip=True)
data = data.split("|")

# Verwijder onodige data
for i in range(0, 28):
  data.pop(0)

# Voeg de seizoenen en speeldagen in aparte lijsten
seizoenen = [0] * 64

for i in range(0, 64):
  seizoenen[i] = data.pop(0)

data.pop(0)

speeldagen = [0] * 34

for i in range(0, 34):
  speeldagen[i] = data.pop(0)

# Methode om de data per seizoen en per speeldag te scrapen
def getData():
    # For loop om alle seizoenen te doorlopen
    for year in range (1960, datetime.date.today().year):
        seizoen = seizoenen.pop()
        # For loop om alle speeldagen te doorlopen voor elk seizoen
        for day in range (1, 35):
          speeldag = speeldagen[day-1]
          URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltagtabelle/wettbewerb/BE1?saison_id={year}&spieltag={day}"
          headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
          page= requests.get(URL, headers=headers)
          soup= BeautifulSoup(page.content, "html.parser")

          prepareData(soup, year, day)
    print("Done")

# Methode die de data schrijft naar het klassementen.csv file
def writeData(seizoen, speeldag, stand, clubnaam, gespeeldeMatchen, gewonnenMatchen, gelijkspeeldeMatchen, verlorenMatchen, doelpunten, puntenverschil, punten):
    with open('klassementen.csv', 'a', newline='\n') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([seizoen, speeldag, stand, clubnaam, gespeeldeMatchen, gewonnenMatchen, gelijkspeeldeMatchen, verlorenMatchen, doelpunten, puntenverschil, punten])

# Methode om de data te scheiden
def prepareData(soup, seizoen, speeldag):
  
  # Soup select om alle tabellen te scrapen
  table = soup.select("#main main div.row div.box:nth-of-type(3) table tbody tr")

  # Split de data
  data = ""
  for row in table:
    data += row.get_text("|", strip=True)
  data = data.split("|")

  # Decraleer variabelen
  stand = ""
  clubnaam = ""
  gespeeldeMatchen = ""
  gewonnenMatchen = ""
  gelijkspeeldeMatchen = ""
  verlorenMatchen = ""
  doelpunten = ""
  puntenverschil = ""
  punten = ""
  i = 0

  # While loop om de data per row weg te schrijven
  while (len(data) > 0):

          stand = ""
          if len(data) < 1:
            break
          if i == 0:
            stand = data.pop(0)
            vorigeStand = stand
          else:
            if int(vorigeStand) >= 9:
              stand+= placeholder[-2]
              stand+= placeholder[-1]
            else:
              stand = placeholder[-1]
          vorigeStand = stand
          if len(data) < 1:
            break
          clubnaam = data.pop(0)
          if len(data) < 1:
            break
          gespeeldeMatchen = data.pop(0)
          if len(data) < 1:
            break
          gewonnenMatchen = data.pop(0)
          if len(data) < 1:
            break
          gelijkspeeldeMatchen = data.pop(0)
          if len(data) < 1:
            break
          verlorenMatchen = data.pop(0)
          if len(data) < 1:
            break
          doelpunten = data.pop(0)
          if len(data) < 1:
            break
          puntenverschil = data.pop(0)
          if len(data) < 1:
            break
          punten = data.pop(0)
          placeholder = punten
          if int(vorigeStand) < 16:
            if int(vorigeStand) >= 9:
                punten = punten[:-2]
            else:
                punten = punten[:-1]


          writeData(seizoen, speeldag, stand,  clubnaam, gespeeldeMatchen, gewonnenMatchen, gelijkspeeldeMatchen, verlorenMatchen, doelpunten, puntenverschil, punten)
          i+=1

# roep de methode getData() op
getData()