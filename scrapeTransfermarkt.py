import requests
from bs4 import BeautifulSoup
import json 
import jmespath
import datetime
import csv

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
     datum = ""
     tijd= ""
     huisploeg = ""
     standThuisploeg = ""
     standUitploeg = ""
     uitploeg = ""

     table = soup.select("#main main div.row div.box:nth-of-type(2) table tbody tr")

     for row in table:
          tds = row.find_all('td', class_=["hide-for-small","zentriert"], )
          print(tds)
          
prepareData()

def writeData(datum, tijd, huisploeg, standThuisploeg, standUitploeg, uitploeg):
    with open('data.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([datum, tijd, huisploeg, standThuisploeg, standUitploeg, uitploeg])



getData()