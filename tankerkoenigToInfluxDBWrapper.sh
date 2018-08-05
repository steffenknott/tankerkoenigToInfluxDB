#!/bin/bash
PATH=/usr/local/bin:$PATH
pipenv run python tankerkoenigToInfluxDB.py >/dev/null 2>&1