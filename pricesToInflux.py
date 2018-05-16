# Modul: pricesToInflux
# Date: 16.05.2018
# Author: steffenknott - Steffen Knott
# Summary: Modul to fetch prices and push then into an InfluxDB instance.

import requests
import json
from influxdb import InfluxDBClient

client = InfluxDBClient("host", 8086, "user", "password", "database")
PRICES_API_URL = "https://creativecommons.tankerkoenig.de/json/prices.php"
APIKEY = "yourkey"

def getPrices (stations):
  try:
    payload = {'ids': ",".join(stations), 'apikey': APIKEY}
    response = requests.get(PRICES_API_URL, params=payload)
    if response.ok:
      return response.json()
    else:
      return None
      print("Error fetching data")
  except Exception as exc:
    print ("Exception while fetching data" + exc)
    quit()

def create_json_stub (station):
  json_item = {}
  json_item.update({"measurement": "spritpreise"})
  json_item.update({"tags": {"tankstelle": station} })
  json_item.update({"fields": {} })
  return json_item

def writePrices (jsonData, sorten):
  json_body = []
  for station in jsonData['prices']:
    json_item = create_json_stub (station)
    for sorte in sorten:
      json_item['fields'].update({sorte: float(jsonData['prices'][station][sorte]) })
    json_body.append(json_item)
    client.write_points(json_body)

# Creating two-dimensional array with stations

stations = []
chunkindex = 0
stations.append([])
with open('tankstellen.conf','r') as stationsfile:
  for station in stationsfile:
    if len(stations[chunkindex]) == 10:
      chunkindex = chunkindex + 1
      stations.append([])
    stations[chunkindex].append(station.rstrip())

# Creating array with fuels of interest
sorten = []
with open('sorten.conf','r') as sortenfile:
  for sorte in sortenfile:
    sorten.append(sorte.rstrip())

# Creating API requests and processing returned data

for station in stations:
  jsonData = getPrices(station)
  output = writePrices(jsonData, sorten)
