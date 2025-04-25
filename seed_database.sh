#!/bin/bash

rm db.sqlite3
rm -rf ./rootedapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations rootedapi
python3 manage.py migrate rootedapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

