#!/usr/bin/env bash

# runtests.sh
# The runtests.sh script is a Bash script that can be used to run the test suite for the "Devlog" project. This script can be helpful for quickly running tests during development without having to remember the individual command.

# Functions
# The runtests.sh script consists of a single command that performs the following steps:

# Clears and resets the terminal screen using clear and reset.
# Runs the Django test suite using python manage.py test with the --failfast flag, which stops the test suite as soon as the first test fails.
# Usage
# To use the runtests.sh script, simply navigate to the directory where the script is located and run the following command:


# ./runtests.sh

# This will execute the script and run the test suite for the "Devlog" project.

clear; reset;
python manage.py test --failfast
