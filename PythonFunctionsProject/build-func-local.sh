#!/bin/bash

# Build the Function locally (install requirements), so that the Function App
# can be tested locally with 'func start' or './start-func-local.sh'.
# Chris Joakim, Microsoft, 2020/05/12
#
# https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python

source ../env.sh 

echo 'using project venv ...'
cd .. 
source bin/activate
cd PythonFunctionsProject

echo 'pip install to .python_packages/lib/site-packages ...'
pip install  --target=".python_packages/lib/site-packages" --upgrade -r requirements.txt

# The above is better than doing this:
# pip install -r requirements.txt
# pip list

echo 'listing directories/packages in .python_packages/lib/site-packages:'
ls -al .python_packages/lib/site-packages

#func azure functionapp publish $app_name --build local

echo 'next:'
echo 'func start'
echo ''
