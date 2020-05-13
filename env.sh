#!/bin/bash

# This bash script defines common configuration, and  is "sourced"
# by the other bash scripts in this directory.
# Chris Joakim, Microsoft, 2020/05/13

export rg=cjoakimfdp
export region=eastus
export storage_name=cjoakimdfpstor
export plan_name=cjoakimdfpsplan
export app_name=cjoakimfdp
export worker_count=1
export image_name="cjoakim/azurepythonfunctions:v1.0.0"
export storage_conn_str="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=cjoakimdfpstor;AccountKey=6C58fDG4/sLBlmehTjlpBe8ViPf68vNELzJC5EJLefwCw2/jDTAFgfz+7afYYkbFzA2umRCND6Wb/Q5rQDtrqg=="

arg_count=$#
if [ $arg_count -gt 0 ]
then
    if [ $1 == "display" ] 
    then
        echo "rg:           "$rg
        echo "region:       "$region
        echo "storage_name: "$storage_name
        echo "plan_name:    "$plan_name
        echo "app_name:     "$app_name
        echo "worker_count: "$worker_count
        echo "image_name:   "$image_name
    fi
fi
