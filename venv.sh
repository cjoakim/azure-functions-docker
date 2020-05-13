#!/bin/bash

# Create a Python 3 Virtual Environment when this project is initially created.
# Chris Joakim, Microsoft, 2020/05/11

echo 'Creating and activating python virtual environment for this Azure Function App:'
python3 -m venv .
source bin/activate

echo 'Displaying python and pip version in virtual environment:'
python --version  
pip --version
pip list

echo 'done'
