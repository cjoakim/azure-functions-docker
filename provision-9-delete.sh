#!/bin/bash

# Delete the Azure Resource Group, and all of its' contents.
# Chris Joakim, Microsoft, 2020/05/12

source ./env.sh display

echo 'az group delete: '$rg
az group delete --name $rg --yes --no-wait

echo 'done'
