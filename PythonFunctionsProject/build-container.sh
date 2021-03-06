#!/bin/bash

# Build the Docker container locally.
# Chris Joakim, Microsoft, 2020/05/12

source ../env.sh 

# example:
# docker build --tag cjoakim/azurepythonfunctions:v1.0.2 .

docker build --tag $image_name .

echo 'next:'
echo 'docker run -p 3000:80 -it '$image_name
echo 'docker push '$image_name
echo ''

# docker container ls --all
# docker rm practical_archimedes
# docker rmi cjoakim/azurepythonfunctions:v1.0.2
 