#!/usr/bin/env bash

# reset.sh
# The reset.sh script is a Bash script that can be used to reset the data for the "Devlog" project. This script can be useful during development to quickly reset the database and migrate data back in from a backup fixture file.

# Configuration
# Before running the script, there are a few configuration options you may want to modify:

# DB_NAME: The name of the Postgres database to reset.
# DB_OWNER: The owner of the Postgres database to reset.
# POSTGRESQL_SERVICE: The name of the Postgres service to restart when resetting the database.
# APPS: An array of app names to reset. These should correspond to the directories inside the apps directory.
# Functions
# The reset.sh script consists of several functions that perform different steps of the reset process:

# set_shell(): Sets the virtual environment shell for the project, if needed.
# dump_data(): Dumps the current data in the database to a fixture file.
# restart_postgresql(): Restarts the Postgresql service.
# recreate_db(): Drops and recreates the database.
# reset_migrations(): Deletes all migration files for each app, creates new migration files, and applies those migrations to the database.
# load_data(): Loads the data from the fixture file back into the database.
# main(): Runs each of the above functions in sequence to reset the data for the project.
# Usage
# To use the reset.sh script, simply navigate to the directory where the script is located and run the following command:

# ./reset.sh

# For Postgreql Only
# Can be edited for each project
DB_NAME="devlog"
DB_OWNER="admin"
POSTGRESQL_SERVICE="postgresql"
APPS=(projects tasks)

# Edit these sparingly
TS=$(date +%d%h%y-%H%M%S)

FIXTURES_DIR="./fixtures"
FIXTURES_DATA_FILE="$FIXTURES_DIR/data_dump.json"
BACKUP_FIXTURES_FILE="$FIXTURES_DIR/backups/data_dump.$TS.json"

set_shell() {
    echo "* Setting venv shell if needed ..."
    cd ..
    pipenv shell
    cd devlog
    echo "* DONE"
}

dump_data() {
    echo "* Dumping data ..."
    python manage.py dumpdata > $FIXTURES_DATA_FILE
    cp $FIXTURES_DATA_FILE $BACKUP_FIXTURES_FILE
    echo "* DONE"
}

restart_postgresql() {
    echo "* Restarting Postgresql ..."
    sudo systemctl restart $POSTGRESQL_SERVICE
    echo "* DONE"
}

recreate_db() {
    echo "* Recreating database ..."
    restart_postgresql;
    sudo su - postgres -c "dropdb $DB_NAME"
    sudo su - postgres -c "createdb $DB_NAME -O $DB_OWNER"
    echo "* DONE"
}

reset_migrations() {
    echo "* Resetting migrations ..."
    for app in "${APPS[@]}"
    do
        rm -rf apps/$app/migrations/*
    done
    
    python manage.py makemigrations

    for app in "${APPS[@]}"
    do
        python manage.py makemigrations $app
    done
    
    python manage.py migrate
    echo "* DONE"
}

load_data() {
    echo "* Loading data ..."
    python manage.py loaddata $FIXTURES_DATA_FILE
    echo "* DONE"
}

main() {
    echo "** Resetting project database(s)"
    clear; reset;
    set_shell;
    dump_data;
    recreate_db;
    reset_migrations;
    load_data;
    echo "** DONE"
}

main
