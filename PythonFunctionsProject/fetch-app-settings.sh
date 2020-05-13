#!/bin/bash

# Download the Azure Function settings, overlay local file 'local.settings.json'.
# Chris Joakim, Microsoft, 2020/05/13

source ../env.sh 

echo 'removing local.settings.json:'
rm local.settings.json

echo 'func azure functionapp list-functions: '$app_name
func azure functionapp list-functions cjoakimfdp --show-keys

echo 'func azure functionapp fetch-app-settings: '$app_name
func azure functionapp fetch-app-settings $app_name

echo 'cat local.settings.json:'
cat local.settings.json

echo 'done'
