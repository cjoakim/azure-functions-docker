#!/bin/bash

# Start the Function App locally, not using Docker, for workstation testing.
# Chris Joakim, Microsoft, 2020/05/12

source bin/activate

echo 'python --version:'
python --version
pip list
echo '============================================================'

func start --python
