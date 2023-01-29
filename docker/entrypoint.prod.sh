#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py makemigrations
python manage.py makemigrations core
python manage.py makemigrations projects
python manage.py makemigrations sprints
python manage.py makemigrations tasks
python manage.py makemigrations ui
python manage.py migrate

exec "$@"
