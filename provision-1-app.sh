#!/bin/bash

# Provision an Azure Resource Group, Storage Account, App Plan, 
# and Azure Function using the Azure CLI (az).
# Chris Joakim, Microsoft, 2020/05/12

source ./env.sh display

echo 'az group create: '$rg
az group create --name $rg --location $region

echo 'sleeping...'
sleep 20

echo 'az storage account create: '$storage_name
az storage account create \
    --name $storage_name \
    --location $region \
    --resource-group $rg \
    --sku Standard_LRS

echo 'sleeping...'
sleep 20

echo 'az functionapp plan create: '$plan_name
az functionapp plan create \
    --resource-group $rg \
    --name $plan_name \
    --location $region \
    --number-of-workers $worker_count \
    --sku EP1 \
    --is-linux

echo 'sleeping...'
sleep 20

echo 'az functionapp create: '$app_name
az functionapp create \
    --name $app_name \
    --storage-account $storage_name \
    --resource-group $rg \
    --plan $plan_name \
    --functions-version 2 \
    --deployment-container-image-name $image_name

echo 'done'
