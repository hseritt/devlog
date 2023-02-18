#!/usr/bin/env bash

# test-down.sh
# The test-down.sh script is a Bash script that can be used to shut down the Docker containers used for running tests for the "Devlog" project. This script can be helpful for quickly shutting down the test environment after running tests.

# Functions
# The test-down.sh script consists of a single command that performs the following steps:

# Uses sudo docker-compose to shut down the Docker containers defined in the docker-compose.test.yml file located in the docker directory.
# Usage
# To use the test-down.sh script, simply navigate to the directory where the script is located and run the following command:

# bash
# Copy code
# ./test-down.sh
# This will execute the script and shut down the Docker containers used for running tests for the "Devlog" project.

sudo docker-compose -f docker/docker-compose.test.yml down 

