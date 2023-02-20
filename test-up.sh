#!/usr/bin/env bash

# test-up.sh
# The test-up.sh script is a Bash script that can be used to set up and start the Docker containers used for running tests for the "Devlog" project. This script can be helpful for quickly setting up the test environment before running tests.

# Functions
# The test-up.sh script consists of several commands that perform the following steps:

# Generates a requirements.txt file based on the current Pipenv environment using pipenv requirements.
# Copies the apps, config, manage.py, staticfiles, templates, and docker directories to the docker directory using cp -rf.
# Uses docker-compose to build and start the Docker containers defined in the docker-compose.test.yml file located in the docker directory.

# Usage
# To use the test-up.sh script, simply navigate to the directory where the script is located and run the following command:

# ./test-up.sh

# This will execute the script and set up the Docker containers used for running tests for the "Devlog" project.

pipenv requirements > docker/requirements.txt
rm -rf docker/apps docker/config docker/manage.py docker/staticfiles docker/templates
cp -rf apps config manage.py staticfiles templates docker/.
docker-compose -f docker/docker-compose.test.yml up --build

