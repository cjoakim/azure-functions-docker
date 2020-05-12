#!/bin/bash

# Build the Function locally (install requirements), so that the Function App
# can be tested locally with 'func start'.
# Chris Joakim, Microsoft, 2020/05/12
#
# https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python

source ../env.sh 

func azure functionapp publish $app_name --build local

echo 'next:'
echo 'func start'
echo ''
