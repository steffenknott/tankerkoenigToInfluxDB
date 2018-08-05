# tankerkoenigToInfluxDB
Small script that pulls gas prices from Tankerkönig and writes them into an InfluxDB

## Requirements

- Python 3 (may work with Python 2 - didn't test it). Optional: I recommend the use of [pipenv](https://robots.thoughtbot.com/how-to-manage-your-python-projects-with-pipenv) which can be installed with ``pip3 install pipenv``. This keeps your python installation clean if you use several different python versions and modules.
- Tankerkönig API Access - you need to register for an API Key at https://creativecommons.tankerkoenig.de
- [influxdb](https://github.com/influxdata/influxdb-python) python package
- A running InfluxDB instance

## Setup

- Rename or create a copy of the `.example`files, which should be edited now to your needs:
- Set proper values in tankerkoenigToInfluxDB.conf
- Lookup gas stations GUIDs [here](https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html) and add them to stations.conf. Be aware that you don't add empty lines to this files, as they will be interpreted as invalid UUIDs

## What the script does

The scripts loads all available gas prices for each gas station listed in stations.conf from the tankerkönig API. Then, it writes them to InfluxDB.

## Run the script

Run ``pipenv install`` to install all requirements. You can enter the environment with ``pipenv shell``. In this shell you can now run the script with ``python tankerkoenigToInfluxDB.py``. You can also run the python script directly with ``tankerkoenigToInfluxDB.py``, but you have to make the script executable first: `chmod +x tankerkoenigToInfluxDB.py`


You can add the script to your crontab to run it every 5 minutes or so:

`*/5 * * * * /path/to/tankerkoenigToInfluxDB.py >/dev/null 2>&1`

If you want to use the python virtual environment provided by pipenc you should add this script:

`*/5 * * * * /path/to/tankerkoenigToInfluxDBWrapper.sh >/dev/null 2>&1`

Make sure that you adjust the path to your installation of the script correctly. It is currently set to ``/path/to/tankerkoenigToInfluxDB``. Depending on your configuration you'll might need to add the path to the pipenv executable to the PATH variable of the ``tankerkoenigToInfluxDBWrapper.sh`` script.


