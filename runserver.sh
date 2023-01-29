#!/usr/bin/env bash

cd ..
pipenv shell
cd devlog

python manage.py makemigrations &&
python manage.py migrate &&
python manage.py runserver

