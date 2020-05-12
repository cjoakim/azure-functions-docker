#!/bin/bash

# Start the Function App locally, not using Docker, for workstation testing.
# Chris Joakim, Microsoft, 2020/05/12

echo 'using project venv ...'
cd .. 
source bin/activate
cd PythonFunctionsProject

echo 'func start ...'
func start
