# tankerkoenigToinfluxDB
Small script that pulls gas prices from Tankerkönig and writes them into an InfluxDB

## Requirements

- Python 3 (may work with Python 2 - didn't test it)
- Tankerkönig API Access - you need to register for an API Key at https://creativecommons.tankerkoenig.de
- [influxdb](https://github.com/influxdata/influxdb-python) package
- A running InfluxDB instance

## Setup

- Set proper values in tankerkoenigToInfluxDB.conf
- Lookup gas stations GUIDs [here](https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html) and add them to stations.conf. 

## What the script does

The scripts loads all available gas prices for each gas station listed in stations.conf from the tankerkönig API. Then, it writes them to InfluxDB.

## Run the script

Run the script like `python3 tankerkoenigToInfluxDB.py`. 

You can add the script to your crontab to run it every 5 minutes or so:

`*/5 * * * * /path/to/tankerkoenigToInfluxDB.py >/dev/null 2>&1`

You have to make the script executable first: `chmod +x tankerkoenigToInfluxDB.py`
