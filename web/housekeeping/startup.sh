#!/bin/bash
sleep 15
python manage.py makemigrations accounts
python manage.py migrate
python manage.py check_permissions
python manage.py cities --import=country --force
echo "removing extra countries"
python manage.py removecountries
echo "importing cities"
python manage.py cities --import=city
python manage.py cities --import=postal_code
echo "starting dev server"
python manage.py runserver 0.0.0.0:8000 