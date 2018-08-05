#!/bin/bash
PATH=/usr/local/bin:$PATH
cd /path/to/tankerkoenigToInfluxDB
pipenv run python tankerkoenigToInfluxDB.py >/dev/null 2>&1