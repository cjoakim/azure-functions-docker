#!/bin/bash

# Configure the Azure CosmosDB Account used by the Function App.
# Chris Joakim, Microsoft, 2020/05/13

source ./env.sh display

echo 'az functionapp config appsettings set: '$app_name
az functionapp config appsettings set \
--name $app_name \
--resource-group $rg \
--settings AzureCosmosDBConnectionString=$AZURE_COSMOSDB_SQLDB_CONN_STRING

echo 'sleeping...'
sleep 20

echo 'az functionapp config appsettings list: '$app_name
az functionapp config appsettings list \
--name $app_name \
--resource-group $rg

echo 'done'
