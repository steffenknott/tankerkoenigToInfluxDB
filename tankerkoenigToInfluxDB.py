#!/usr/bin/env python
# Modul: tankerkoenigToInfluxDB.py
# Date: 16.05.2018
# Author: steffenknott - Steffen Knott
# Summary: Script to fetch prices and push then into an InfluxDB instance.

# This script queries gas prices from the tankerkoenig API and pushes them to
# influxDB. You need an API Key from tankerkoenig. A list of gas station GUIDs
# has to be put into a file called 'tankstellen.conf' in the script dir. All available
# gas types will be processed.

import requests
import json
from influxdb import InfluxDBClient
import os
from os.path import exists

config = {
    "influxHost" : "",
    "influxPort" : 8086,
    "influxUsername" : "",
    "influxPassword" : "",
    "influxDatabase" : "",
    "influxMeasurement" : "",
    "influxStationIdTagName" : "",
    "tankerkoenigApikey" : "",
    "tankerkoenigChunkSize" : "",
    "debugMode" : False
}
configFile = os.path.dirname(os.path.realpath(__file__)) + "/tankerkoenigToInfluxDB.conf"

if exists(configFile) :
    with open(configFile, "r") as f:
        config.update({k:v for k,v in json.loads(f.read()).items()})

client = InfluxDBClient(config['influxHost'], config['influxPort'], config['influxUsername'], config['influxPassword'], config['influxDatabase'])
PRICES_API_URL = "https://creativecommons.tankerkoenig.de/json/prices.php"


def getPrices (stations):
  try:
    if config['debugMode']:
      print ("Querying API for: " + ",".join(stations))
      print ()
    payload = {'ids': ",".join(stations), 'apikey': config['tankerkoenigApikey']}
    response = requests.get(PRICES_API_URL, params=payload)
    if response.ok:
      if response.json()["ok"]:
        if config['debugMode']:
          print ("API RESPONSE: {0}".format(response.json()))
          print ()
        return response.json()
      else:
        print("API responded with error: " + response.json()["message"])
        return None
    else:
      print("Error fetching data")
      quit()
  except Exception as exc:
    print ("Exception while fetching data" + exc)
    quit()

def create_json_stub (station):
  json_item = {}
  json_item.update({"measurement": config['influxMeasurement']})
  json_item.update({"tags": {config['influxStationIdTagName']: station} })
  json_item.update({"fields": {} })
  return json_item

def writePrices (jsonData):
  json_body = []
  for station in jsonData['prices']:
    if config['debugMode']:
      print ("Processing record for station: " + station)
    json_item = create_json_stub (station)
    for sorte in jsonData['prices'][station]:
      if sorte=="status":
        if jsonData['prices'][station][sorte] == "open":
          json_item['fields'].update({"status": 1 }) #open
        elif jsonData['prices'][station][sorte] == "closed":
          json_item['fields'].update({"status": 0 }) #closed
        else:
          json_item['fields'].update({"status": -1 }) #no prices
      else:
          json_item['fields'].update({sorte: float(jsonData['prices'][station][sorte]) })
    if config['debugMode']:
      print ("JSON for item: {0}".format(json_item))
    json_body.append(json_item)
  if config['debugMode']:
    print()
    print("INFLUX INSERT JSON BODY: {0}".format(json_body))
    print()
  client.write_points(json_body)

# Creating two-dimensional array with stations

stations = []
chunkindex = 0
stations.append([])
with open(os.path.dirname(os.path.realpath(__file__)) + '/stations.conf','r') as stationsfile:
  for station in stationsfile:
    if len(stations[chunkindex]) == config['tankerkoenigChunkSize']:
      chunkindex = chunkindex + 1
      stations.append([])
    stations[chunkindex].append(station.rstrip())

# Creating API requests and processing returned data

for station in stations:
  jsonData = getPrices(station)
  output = writePrices(jsonData)
