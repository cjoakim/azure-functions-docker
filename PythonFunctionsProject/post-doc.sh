#!/bin/bash

# Use curl to HTTP POST data to the Function.
# Chris Joakim, Microsoft, 2020/05/13

hdr='Content-type: application/json'
url="http://localhost:7071/api/PyHttp1"

echo '{"pk":"CLT", "client":"curl"}' | curl -i -X POST -H $hdr -d @- $url

