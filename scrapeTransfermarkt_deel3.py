# Deel 3

# Used imports
import requests
from bs4 import BeautifulSoup
import datetime
import csv
import re

# 
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
        for day in range (1, 2):
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

     months = ["sep", "okt", "nov", "dec", "jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug"]

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
     
     print(ploegData)

     table = soup.select("#main main div.row div[class='large-8 columns'] table tbody tr td[class='zentriert no-border']")

     tijdData = ""
     for row in table:
          tijdData += row.get_text("|", strip=True)
     tijdData = tijdData.split("|")
     
     new_data = []
     for x in tijdData:
      new_data.extend(re.split(r"([0-9]+:[0-9]+)", x))
     tijdData = new_data

     x = 0
     while (x < len(tijdData)-1):
      if x >= len(tijdData):
        pass
      elif len(tijdData[x]) <= 2:
        tijdData.remove(tijdData[x])
        x -= 1
      elif tijdData[x].startswith('-'):
        tijdData.remove(tijdData[x])
        x -= 1
      elif 'uur' in tijdData[x]:
        tijdData.remove(tijdData[x])
        x -= 1
      elif 'Spelverloop' in tijdData[x]:
        tijdData.remove(tijdData[x])
        x -= 1
      elif '%' in tijdData[x]:
        tijdData.remove(tijdData[x])
        x -= 1
      x += 1
     
     dagen = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
     i=0
     while i<len(tijdData):
      if any(dag in tijdData[i] for dag in dagen):
        tijdData.pop(i)
      i+=1
     tijdData.pop()
     tijdData.pop()
     print(tijdData)

     table = soup.select("#main main div.row div[class='large-8 columns'] table tbody tr[class='no-border spieltagsansicht-aktionen']")

     scoreData = ""
     for row in table:
          scoreData += row.get_text("|", strip=True)
     scoreData = scoreData.split("|")
     
     new_data = []
     for x in scoreData:
      new_data.extend(re.split(r"([0-9]:[0-9])", x))
     scoreData = new_data
     
     tempdata = []
     for i in range(0,len(scoreData)-1):
        if re.match("[\W\d]+", scoreData[i]):
          tempdata.append(scoreData[i])
     
     print(tempdata)

    #  for x in range(0, len(data)-1):
    #     if x >= len(data):
    #       break
    #     if re.match("[0-9]{2}:[0-9]{2}..", data[x]):
    #       data.remove(data[x])

    #  for x in range(0, len(data)-1):
    #     if x >= len(data)-1:
    #       break
    #     if data[x] == data[x+1]:
    #       data.remove(data[x])    

    #  new_data = []
    #  for x in data:
    #   new_data.extend(re.split(r"([0-9]+:[0-9]+)", x))
    #  data = new_data

    #  x = 0
    #  while (x < len(data)-1):
    #   if x >= len(data):
    #     pass
    #   elif len(data[x]) <= 2:
    #     data.remove(data[x])
    #     x -= 1
    #   elif data[x].startswith('-'):
    #     data.remove(data[x])
    #     x -= 1
    #   elif 'uur' in data[x]:
    #     data.remove(data[x])
    #     x -= 1
    #   elif 'Spelverloop' in data[x]:
    #     data.remove(data[x])
    #     x -= 1
    #   elif '%' in data[x]:
    #     data.remove(data[x])
    #     x -= 1
    #   x += 1
      
    # #  print(data)

    #  while (len(data) > 0):
    #         item = data.pop(0)
    #         if any(month in item for month in months):
    #             datum = item.strip()
    #         if re.match(r"\d{2}:\d{2}", item):
    #             tijd = item.strip()
    #         if re.search(r"saison_id/(\d{4})", URL):
    #           jaar = re.search(r"saison_id/(\d{4})", URL).group(1)
    #         if re.search(r"spieltag/(\d+)", URL):
    #           speeldag = re.search(r"spieltag/(\d+)", URL).group(1)

    #         if ":" in item:
    #           standThuisploeg = item[0]
    #           standUitploeg = item[2]
    #           if "'" in data[0]:
    #                 tijdstipDoelpunt = data[0]
    #           if data and data[0].isdigit():
    #             scorendePloeg = uitploeg
    #           else:
    #             scorendePloeg = huisploeg
            # print(f"speeldag: ", speeldag)
            # print(f"jaar: ", jaar)
            # print(f"datum: ", datum)
            # print(f"tijd: ", tijd)
            # print(f"afkortingHuisploeg: ", afkortingHuisploeg)
            # print(f"huisploeg: ", huisploeg)
            # print(f"afkortingUitploeg: ", afkortingUitploeg)
            # print(f"Uitploeg: ", uitploeg)
            # print(f"tijdstipdoelpunt: ", tijdstipDoelpunt)


            # print(f"huisstand: ", standThuisploeg)
            # print(f"uitsstand: ", standUitploeg)

    #  while (len(data) > 0):
    #   if any(month in data[0] for month in months):
    #     datum = data.pop(0)
    #   if re.match("[0-9]{2}:[0-9]{2}", data[0]):
    #     tijd = data.pop(0)
    #   afkortingHuisploeg = data.pop(0)
    #   if afkortingHuisploeg == "Standard Luik":
    #     huisploeg = "Standard Luik"
    #   elif afkortingHuisploeg == "Germinal Ekeren":
    #     huisploeg = "Germinal Ekeren"
    #   else:
    #     huisploeg = data.pop(0)
    #   stand = data.pop(0)
    #   print (f"stand: ", stand)
    #   if re.match("^[\d:]+$", stand):
    #     huisstand, uitstand = stand.split(":")
    #   else:
    #     huisstand = 0
    #     uitstand = 0
    #   afkortingUitploeg = data.pop(0)
    #   if afkortingUitploeg == "Standard Luik":
    #     uitploeg = "Standard Luik"
    #   elif afkortingUitploeg == "Germinal Ekeren":
    #     uitploeg = "Germinal Ekeren"
    #   else:
    #     uitploeg = data.pop(0)  

    #  print(f"speeldag: ", speeldag)
    #  print(f"jaar: ", jaar)
    #  print(f"datum: ", datum)
    #  print(f"tijd: ", tijd)
    #  print(f"afkortingHuisploeg: ", afkortingHuisploeg)
    #  print(f"huisploeg: ", huisploeg)
    #  print(f"afkortingUitploeg: ", afkortingUitploeg)
    #  print(f"Uitploeg: ", uitploeg)
    #  print(f"tijdstipdoelpunt: ", tijdstipDoelpunt)


    #  print(f"huisstand: ", standThuisploeg)
    #  print(f"uitsstand: ", standUitploeg)


getData()