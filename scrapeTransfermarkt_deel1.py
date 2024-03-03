# Used imports 
import requests
from bs4 import BeautifulSoup
import datetime
import csv
import re

# Methode om de data per seizoen en per speeldag te scrapen
def getData():
    # For loop om alle seizoenen te doorlopen
    for year in range (1960, datetime.date.today().year):
        seizoen = (str(year)[2:] + "/" + str(year + 1)[2:])
        # For loop om alle speeldagen te doorlopen voor elk seizoen
        for day in range (1, 35):
          speeldag = day
          URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltagtabelle/wettbewerb/BE1?saison_id={year}&spieltag={day}"
          headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
          page= requests.get(URL, headers=headers)
          soup= BeautifulSoup(page.content, "html.parser")
          prepareData(soup, seizoen, speeldag)
    print("Done")
# Methode die de data schrijft naar het wedstrijden.csv file
def writeData(id, seizoen, speeldag, datum, tijd, huisploeg, huisstand, uitstand, uitploeg):
    #with open('test.csv', 'a', newline='\n') as file:
    with open('voetbalData_Deel2.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([id, seizoen, speeldag, datum, tijd, huisploeg, huisstand, uitstand, uitploeg])

def changeDateFormat(datum):
    maand_afkortingen = {
        "jan.": "01",
        "feb.": "02",
        "mrt.": "03",
        "apr.": "04",
        "mei": "05",  
        "jun.": "06",
        "jul.": "07",
        "aug.": "08",
        "sep.": "09",
        "okt.": "10",
        "nov.": "11",
        "dec.": "12"
    }
    dag, maand, jaar = datum.split()
    maand = maand_afkortingen[maand.lower()]
    print(dag)
    return f"{dag}/{maand}/{jaar}"

# Methode om de data te scheiden
def prepareData(soup, seizoen, speeldag):
  
  # Decraleer variabelen
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

  # Soup selects
  table = soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr")
  idstext = soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr td span a[title='Wedstrijdverslag']")
  idstext += soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr td span a[title='Voorbeschouwing']")

  # Haal alle id's op
  ids = []
  for a in idstext:
    href = a['href']
    if re.match(r'/spielbericht/index/spielbericht/(\d+)', href):
      ids.append(str(re.findall(r'\d+', href)))
  ids.sort()
  
  # Split de data
  data = ""
  for row in table:
      data += row.get_text("|", strip=True)
  data = data.split("|")

  # Verwijder foute data
  for x in data:
      if "." in x and "(" in x:
            data.remove(x)

  # Verwijder lege values
  if data == ['']:
    return
  
  # Verwijder de onnodige data
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

  # While loop om de data op te halen en weg te schrijven
  while (len(data) > 0):
    if any(month in data[0] for month in months):
        datum = changeDateFormat(data.pop(0))
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
    if stand != "verplaatst":
      id = ids.pop(0)[2:-2]
    else:
      id = "-"
    if id == "" or datum == "" or tijd == "" or speeldag == "" or seizoen == "":
       print("Er is iets foutgelopen")
       print(id, seizoen, speeldag, datum, tijd, huisploeg, huisstand, uitstand, uitploeg)
       quit

    writeData(id, seizoen, speeldag, datum, tijd, huisploeg, huisstand, uitstand, uitploeg)
      
getData()