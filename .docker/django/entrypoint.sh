#!/bin/bash

# Run migrations
python manage.py migrate --no-input

# Populate Cities-Light
python manage.py cities_light

# Collect static files
python manage.py collectstatic --no-input

# Start server
if [[ ${ENVIRONMENT} = 'production' ]]; then
    gunicorn api.wsgi:application --workers 4 --bind "0.0.0.0:8000"
else
    python manage.py runserver "0.0.0.0:8000"
fi
