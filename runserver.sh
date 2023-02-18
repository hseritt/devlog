#!/usr/bin/env bash

# runserver.sh
# The runserver.sh script is a Bash script that can be used to start the Django development server for the "Devlog" project. This script can be helpful for quickly starting the server during development without having to remember the individual commands.

# Functions
# The runserver.sh script consists of a single command that performs the following steps:

# Changes the current working directory to the parent directory of the project using cd ...
# Activates the Pipenv virtual environment shell for the project using pipenv shell.
# Changes the working directory to the devlog directory, which contains the Django project code using cd devlog.
# Runs three python manage.py commands:
# makemigrations: Creates new migration files based on changes to the models in the project.
# migrate: Applies any outstanding migrations to the database.
# runserver: Starts the Django development server.
# Usage
# To use the runserver.sh script, simply navigate to the directory where the script is located and run the following command:

# ./runserver.sh

cd ..
pipenv shell
cd devlog

python manage.py makemigrations &&
python manage.py migrate &&
python manage.py runserver

