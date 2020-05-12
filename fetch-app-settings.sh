#!/bin/bash

# Download the Azure Function settings, overlay local file 'local.settings.json'.
# Chris Joakim, Microsoft, 2020/05/12

source ./env.sh 

rm local.settings.json

echo 'func azure functionapp fetch-app-settings: '$app_name
func azure functionapp fetch-app-settings cjoakimfdp

mv local.settings.json PythonFunctionsProject/

echo 'downloaded file:'
cat PythonFunctionsProject/local.settings.json

echo 'done'
