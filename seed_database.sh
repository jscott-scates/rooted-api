#!/bin/bash

rm db.sqlite3
rm -rf ./rootedapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations rootedapi
python3 manage.py migrate rootedapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata spreads
python3 manage.py loaddata spread_positions
python3 manage.py loaddata deck_types
python3 manage.py loaddata decks
python3 manage.py loaddata elements
python3 manage.py loaddata card_types
python3 manage.py loaddata keywords
python3 manage.py loaddata cards
python3 manage.py loaddata card_keywords
python3 manage.py loaddata sages
python3 manage.py loaddata journal_entries
python3 manage.py loaddata entry_cards 

