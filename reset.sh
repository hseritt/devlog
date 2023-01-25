#!/usr/bin/env bash

# For Postgreql Only
# Can be edited for each project
DB_NAME="devlog"
DB_OWNER="admin"
POSTGRESQL_SERVICE="postgresql"
APPS=(tasks)

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
