"""
Usage:
  python http-client.py create_config_json
  python http-client.py load_regions local
  python http-client.py query_by_pk local eastus
  python http-client.py query_by_pk local germanynorth
  python http-client.py query_by_geo local 53.073635 8.806422 10
"""

# Python HTTP Client program for this Azure Function.
# Chris Joakim, Microsoft, 2020/05/13

import json
import os
import sys
import time
import uuid 

import requests

from docopt import docopt

VERSION = 'v20200513a'


class HttpClient:

    def __init__(self):
        self.u = None  # the current url
        self.r = None  # the current requests response object
        self.config = self.load_json_file('config.json')
        self.user_agent = {'User-agent': 'Mozilla/5.0'}

    def create_config_json(self):
        data = dict()
        data['local'] = 'http://localhost:7071/api/PyHttp1'
        data['azure'] = ''
        self.write_json_file(data, 'config.json')

    def load_regions(self, target):
        url = self.config[target]
        print('url: {}'.format(url))

        regions = self.load_json_file('data/azure-regions.json')
        for region in regions:
            lat, lng = float(region['latitude']), float(region['longitude'])
            region['doctype'] = 'region'
            region['pk'] = region['name']
            region['lat_lng'] = '{}, {}'.format(lat, lng)
            loc = dict()
            loc['type'] = 'Point'
            loc['coordinates'] = [lng, lat]
            region['location'] = loc
            for attr in 'id,latitude,longitude,subscriptionId'.split(','):
                del region[attr]
            print(json.dumps(region, sort_keys=False, indent=2))
            self.execute_post(url, region, {})

    def query_by_pk(self, target, pk):
        url = self.config[target]
        print('url: {}'.format(url))
        data = dict()
        data['query'] = "select * from c where c.pk = '{}'".format(pk)
        self.execute_post(url, data, {})

    def query_by_geo(self, target, lng, lat, meters):
        url = self.config[target]
        print('url: {}'.format(url))
        template = "select * from c where ST_DISTANCE(c.location, <'{}': 'Point', 'coordinates':[{}, {}]>) | {}"
        sql = template.format('type', lng, lat, meters)
        sql = sql.replace('<','{')
        sql = sql.replace('>','}')
        sql = sql.replace('|','<')
        print(sql)
        data = dict()
        data['query'] = sql
        self.execute_post(url, data, {})

    def execute_post(self, endpoint, postobj, opts):
        print('===')
        print('execute_post, endpoint: {}'.format(endpoint))
        print(json.dumps(postobj, sort_keys=False, indent=2))
        print('')
        r = requests.post(url=endpoint, json=postobj) 
        print('---')
        print('response: {}'.format(r))

        if r.status_code == 200:
            resp_obj = json.loads(r.text)
            print(json.dumps(resp_obj, sort_keys=False, indent=2))

    def write_json_file(self, obj, outfile):
        with open(outfile, 'wt') as f:
            f.write(json.dumps(obj, sort_keys=False, indent=2))
            print('file written: {}'.format(outfile))

    def load_json_file(self, infile):
        with open(infile, 'rt') as json_file:
            return json.loads(str(json_file.read()))

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=VERSION)
    print(arguments)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        client = HttpClient()

        if func == 'create_config_json':
            client.create_config_json()

        elif func == 'load_regions':
            target = sys.argv[2].lower()
            client.load_regions(target)

        elif func == 'query_by_pk':
            target, pk = sys.argv[2].lower(), sys.argv[3]
            client.query_by_pk(target, pk)

        elif func == 'query_by_geo':
            target = sys.argv[2].lower()
            lat = float(sys.argv[3].lower())
            lng = float(sys.argv[4].lower())
            km  = int(sys.argv[5].lower())
            client.query_by_geo(target, str(lat), str(lng), str(km * 1000))
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')