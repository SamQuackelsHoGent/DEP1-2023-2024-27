# Used imports
import requests
from bs4 import BeautifulSoup
import datetime
import csv
import re
import numpy

# Declareer lijst om ploegen in op te slaan
ploegen = []

# Methode om de data te scrapen
def getData():
    # For loop om alle seizoenen te doorlopen
    for year in range (1960, datetime.date.today().year):
        seizoen = (str(year)[2:] + "/" + str(year + 1)[2:])
        # For loop om alle dagen per seizoen te doorlopen.
        for day in range (1, 34):
          # Gebruik soup om data te scrapen
          URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltag/wettbewerb/BE1/saison_id/{year}/spieltag/{day}"
          headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
          page= requests.get(URL, headers=headers)
          soup= BeautifulSoup(page.content, "html.parser")
          # if (day == 33 and seizoen=="81/82"):
          #    print("Ok")
          amountOfGames = 0
          for i in range (0,20):
            possibleData = soup.select(f"#main main div.row div[class='large-8 columns'] div[class='box']:nth-of-type({str(i + 1)}) table tbody tr td span a[title='Wedstrijdverslag']")
            if possibleData == []:
              amountOfGames = i
          getPloegen(soup, seizoen, day)
          for matchcount in range(1,amountOfGames):
            prepareDataMatch(soup, year, day, matchcount)
    print("Done")

# Methode om de data weg te schrijven naar het doelpunten.csv file
def writeData(seizoen, speeldag, datum, tijd, match_id, huisploeg, uitploeg, tijdpunt, tijdstip, goalploeg, newhuisstand, newuitstand):
    with open('doelpunten.csv', 'a', newline='\n') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([seizoen, speeldag, datum, tijd, match_id, huisploeg, uitploeg, tijdpunt, tijdstip, goalploeg, newhuisstand, newuitstand])

# Methode om de verschillende ploegen op te halen
def getPloegen(soup, seizoen, speeldag):
    global ploegen
    table = soup.select("#main main div.row div[class='large-8 columns'] table tbody tr.table-grosse-schrift:nth-of-type(1)")

    ploegData = ""
    for row in table:
        ploegData += row.get_text("|", strip=True)
    ploegData = ploegData.split("|")

    for x in ploegData:
        if "." in x and "(" in x:
              ploegData.remove(x)

    for x in ploegData:
        if ":" in x:
              ploegData.remove(x)
    
    for i in range(1, int(len(ploegData)/2)):
      ploegData.pop(i)
    ploegen= [ploegData[i] for i in range(0, len(ploegData))]

# methode om datum in het goede formaat om te zetten
def changeDateFormat(datum):
    # dict om maanden om te zetten naar nummer formaat
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
    # Veranderd de maand naar het juiste formaat
    dag, maand, jaar = datum.split()
    maand = maand_afkortingen[maand.lower()]
    return f"{jaar}-{maand}-{dag}"

# methode om de data te scrapen
def prepareDataMatch(soup, seizoen, speeldag, matchnumber):
     # declareer de variabelen
     
     global ploegen
     datum = ""
     tijd= ""

     if len(ploegen) > 1:
      huisploeg = ploegen.pop(0)
      uitploeg = ploegen.pop(0)
     else:
      return
     
     if (seizoen == "02/03"):
        if "Lommel" in ploegen or "Moeskroen" in ploegen:
           return

     # Soup om de match id op te halen
     idstext = soup.select(f"#main main div.row div[class='large-8 columns'] div[class='box']:nth-of-type({str(matchnumber + 1)}) table tbody tr td span a[title='Wedstrijdverslag']")
     if idstext == []:
        return
     href = idstext[0]['href']
     # regex om de match id te zoeken
     match = re.search(r'/spielbericht/index/spielbericht/(\d+)', href)
     match_id = ""
     if match:
      match_id = match.group(1)
     
     # Soup om de generieke data op te halen
     table = soup.select(f"#main main div.row div[class='large-8 columns'] div[class='box']:nth-of-type({str(matchnumber + 1)}) > table")
     
     # Steek de data in een list
     data = ""
     for row in table:
       data += row.get_text("|", strip=True)
     data = data.split("|")
     if len(data) <= 1:
        return
     
     # Soup om de tijdstippen op te halen
     table = soup.select(f"#main main div.row div[class='large-8 columns'] div[class='box']:nth-of-type({str(matchnumber + 1)})")
     
     # Steek de tijdstippen in een list
     tijdData = ""
     for row in table:
          tijdData += row.get_text("|", strip=True)
     tijdData = tijdData.split("|")

     # Zoek voor geldige tijdstippen
     for x in tijdData:
        match = re.match(".*[\d]{2}:[\d]{2}.*", x)
        if match:
           tijd = re.search("[\d]{2}:[\d]{2}", x).group()
           break
     
     # Doorloop de genrieke data adhv een while loop
     x = 0
     while x < len(data)-1:
      # Als data leeg is -> break
      if x >= len(data)-1:
          break
      # Verwijder foute data
      if data[x].startswith('-'):
        del data[x]
      # Verwijder foute data
      elif 'uur' in data[x]:
        del data[x]
      # Verwijder foute data
      elif len(data[x]) <= 2:
        del data[x]
      # Verwijder foute data
      elif 'Spelverloop' in data[x]:
        del data[x]
      # Verwijder foute data
      elif '%' in data[x]:
        del data[x]
      # Verwijder foute data
      elif "." in data[x] and "(" in data[x]:
        del data[x]
      # Verwijder foute data
      elif "   " in data[x]:
        del data[x]
      # Verwijder foute data
      # elif any(ploeg in str(data[x]) for ploeg in ploegen):
      #   del data[x]
      # Verwijder foute data
      elif "voorspellingen" in data[x] or "Wedstrijdverslag" in data[x]:
        del data[x]
      else:
         x += 1
     # Ploegen ophalen
     
     # While loop om de doelpunten per match te vinden
     goalData = []
     x = 0
     while x < len(data)-1:
        if re.match("[\W\d]+", data[x]):
           goalData.append(data[x])
        x += 1
     goalData.pop(0)
     datum = changeDateFormat(goalData.pop(0))
     huisstand = 0
     uitstand = 0
     if len(goalData) % 2 != 0:
        return
     # While loop om de doelpunten te doorlopen per match
     i = 0
        # Als er een : teken is -> split de data om de stand te krijgen.
     while i < len(goalData):
        if ":" in goalData[i]:
           standen = goalData[i].split(":")
           newhuisstand = standen[0]
           newuitstand = standen[1]
           
           # Als de thuisploeg scoort
           if int(newhuisstand) > int(huisstand):
              if not "'" in goalData[i-1]:
                 return
              tijdpunt = int(re.search("[\d]*", goalData[i-1]).group())
              minuten = int(tijd.split(":")[0]) * 60 + int(tijd.split(":")[1]) + tijdpunt
              tijdstip = str(int(minuten/60)) + ":" + str(int(minuten % 60))
              tijdstip = datetime.datetime.strptime(tijdstip, "%H:%M")
              tijdstip = tijdstip.strftime("%H:%M")
              # Schrijf de data weg naar de csv file
            #   writeData(match_id, seizoen, speeldag, datum, tijd, huisploeg, uitploeg, huisploeg, tijdpunt, tijdstip, newhuisstand, newuitstand)
              writeData(seizoen, speeldag, datum, tijd, match_id, huisploeg, uitploeg, tijdpunt, tijdstip, huisploeg, newhuisstand, newuitstand)
           
           # Als de uitploeg scoort
           if int(newuitstand) > int(uitstand):
              if not "'" in goalData[i+1]:
                 return
              tijdpunt = int(re.search("[\d]*", goalData[i+1]).group())
              minuten = int(tijd.split(":")[0]) * 60 + int(tijd.split(":")[1]) + tijdpunt
              tijdstip = str(int(minuten/60)) + ":" + str(int(minuten % 60))
              tijdstip = datetime.datetime.strptime(tijdstip, "%H:%M")
              tijdstip = tijdstip.strftime("%H:%M")
              # Schrijf de data weg naar de csv file
            #   writeData(match_id, seizoen, speeldag, datum, tijd, huisploeg, uitploeg, uitploeg, tijdpunt, tijdstip, newhuisstand, newuitstand)
              writeData(seizoen, speeldag, datum, tijd, match_id, huisploeg, uitploeg, tijdpunt, tijdstip, uitploeg, newhuisstand, newuitstand)
           
           huisstand = newhuisstand
           uitstand = newuitstand

        i += 1

getData()