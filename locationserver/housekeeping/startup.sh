#!/bin/bash
sleep 25
python manage.py makemigrations accounts
python manage.py migrate
python manage.py check_permissions
# python manage.py checkcityexists
python manage.py cities --import=country --force
echo "removing extra countries"
python manage.py removecountries
# echo "importing cities"
python manage.py cities --import=city
python manage.py cities --import=postal_code
echo "starting server"
#python manage.py runserver 0.0.0.0:8000 
/usr/local/bin/gunicorn cannablr.wsgi:application -w 2 -b :8000