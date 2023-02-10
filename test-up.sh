#!/usr/bin/env bash

pipenv requirements > docker/requirements.txt
cp -rf apps config manage.py staticfiles docker/.
docker-compose -f docker/docker-compose.test.yml up --build

