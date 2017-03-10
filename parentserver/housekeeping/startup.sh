#!/bin/bash
sleep 15
python manage.py makemigrations accounts
python manage.py migrate
# python manage.py check_permissions
echo "loading fixtures"
# python manage.py loaddata initial_data.json

echo "starting server"
#python manage.py runserver 0.0.0.0:8000 
/usr/local/bin/gunicorn cannablr.wsgi:application -w 2 -b :8000 --preload