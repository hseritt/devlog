#!/usr/bin/env bash

pipenv requirements > docker/requirements.txt
cp -rf apps config manage.py staticfiles docker/.
sudo docker-compose -f docker/docker-compose.prod.yml up --build -d

