#!/bin/bash

# Build the Docker container locally.
# Chris Joakim, Microsoft, 2020/05/11

source ../env.sh 

# example:
# docker build --tag cjoakim/azurepythonfunctions:v1.0.0 .

docker build --tag $image_name .

echo 'next:'
echo 'docker run -p 3000:80 -it '$image_name
echo 'docker push '$image_name
