import requests
from bs4 import BeautifulSoup
import json 
import jmespath
import datetime
import csv
import re

soup = ""

def getData():
    for year in range (2022, datetime.date.today().year - 1):
        for day in range (1, 2):
          URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltagtabelle/wettbewerb/BE1?saison_id={year}&spieltag={day}"
          headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
          page= requests.get(URL, headers=headers)
          soup= BeautifulSoup(page.content, "html.parser")
          # print(soup)
          # prepareData(result)
    print("Done")

def prepareData():

     URL= f"https://www.transfermarkt.be/jupiler-pro-league/spieltagtabelle/wettbewerb/BE1?saison_id=2019&spieltag=13"
     headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Odin/88.4324.2.10 Safari/537.36 Model/Hisense-MT9602 VIDAA/6.0(Hisense;SmartTV;43A53FUV;MTK9602/V0000.06.12A.N0406;UHD;HU43A6100F;)'}
     page= requests.get(URL, headers=headers)
     soup= BeautifulSoup(page.content, "html.parser")
     # print(soup)
     # prepareData(result)
     
     months = ["sep", "okt", "nov", "dec", "jan", "feb", "ma", "apr", "mei", "jun", "jul", "aug"]
     datum = ""
     tijd= ""
     huisploeg = ""
     standThuisploeg = ""
     standUitploeg = ""
     uitploeg = ""

     table = soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr")
     
     data = ""
     for row in table:
          data += row.get_text("|", strip=True)
     data = data.split("|")
     for x in data:
          if "." in x and "(" in x:
               data.remove(x)
     
     for x in range(0, len(data)-1):
          if data[x] == data[x+1]:
               data.remove(x)

     while (len(data) > 0):
          item = data.pop(0)
          if len(item) <= 2:
               continue
          if re.match("[0-9]{2}:[0-9]{2}.*", item):
               continue
          if any(month in item for month in months):
               datum = item
               item = data.pop(0)
          if re.match("[0-9]{2}:[0-9]{2}", item):
               tijd = item
               if re.match(".*[a-z].*", item):
                    tijd = tijd[:-2]
          
          
          

          
          
prepareData()

def writeData(datum, tijd, huisploeg, standThuisploeg, standUitploeg, uitploeg):
    with open('data.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([datum, tijd, huisploeg, standThuisploeg, standUitploeg, uitploeg])



getData()