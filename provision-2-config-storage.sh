#!/bin/bash

# Configure the Azure Storage Account used by the Function App.
# Chris Joakim, Microsoft, 2020/05/12

source ./env.sh display

echo 'az storage account show-connection-string: '$storage_name
az storage account show-connection-string \
--resource-group $rg \
--name $storage_name \
--query connectionString \
--output tsv

# Set env var 'storage_conn_str', in env.sh, from the output of the above.

echo 'sleeping...'
sleep 20

echo 'az functionapp config appsettings set: '$app_name
az functionapp config appsettings set \
--name $app_name \
--resource-group $rg \
--settings AzureWebJobsStorage=$storage_conn_str

echo 'sleeping...'
sleep 20

echo 'az functionapp config appsettings list: '$app_name
az functionapp config appsettings list \
--name $app_name \
--resource-group $rg

echo 'done'
