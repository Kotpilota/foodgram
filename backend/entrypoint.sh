#!/bin/bash

python manage.py migrate

python manage.py load_data_ingredients

# python manage.py collectstatic --noinput

# cp -r /app/collected_static/. /backend_static/static/

exec "$@"