#!/bin/bash

# Activate django .venv

source server/.venv/bin/activate

# Load env file
export $(grep -v '^#' .env | xargs -d '\n')

export DB_HOST=localhost
export DB_PASSWORD=123456
python server/api/manage.py makemigrations
python server/api/manage.py migrate
python server/api/manage.py runserver