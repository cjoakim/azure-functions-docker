"""
Usage:
  python http-client.py create_config_json
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
        self.config = dict()
        self.user_agent = {'User-agent': 'Mozilla/5.0'}

    def create_config_json(self):
        data = dict()
        data['local'] = 'http://localhost:7071/api/PyHttp1'
        data['azure'] = ''
        self.write_json_file(data, 'config.json')

    def post_region_inserts(self, target, infile, pk):
        # target is a partial URL like this: http://52.179.113.199
        # infile is a json file in the journeys directory, like relay-planet-aks.json
        endpoint = '{}/journey/relay'.format(target)
        print('post_journey_relay endpoint: {}'.format(endpoint))
        postobj  = self.load_json_file('journeys/{}'.format(infile))
        postobj['pk'] = pk
        f = 'post_journey_relay_{}'.format(pk)
        self.execute_post(endpoint, postobj, {'f': f})



    def execute_get(self, endpoint, opts=dict()):
        print('execute_get, endpoint: {}'.format(endpoint))
        r = requests.get(url=endpoint) 
        print('response: {}'.format(r))

        if r.status_code == 200:
            resp_obj = json.loads(r.text)
            print(json.dumps(resp_obj, sort_keys=False, indent=2))
            if len(opts.keys()) > 0:
                p = dict()
                p['endpoint'] = endpoint
                p['resp'] = str(r)
                p['resp_obj'] = resp_obj
                outfile = 'tmp/{}_{}.json'.format(int(self.epoch()), opts['f'])
                self.write_json_file(p, outfile)

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
            if 'save_to_file' in opts:
                p = dict()
                p['endpoint'] = endpoint
                p['postobj']  = postobj
                p['resp'] = str(r)
                p['resp_obj'] = resp_obj
                self.write_json_file(p, 'tmp/post.json')

    def epoch(self):
        return time.time()
    
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
    # print(sys.argv)

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        client = HttpClient()
        #client.initialize()

        if func == 'create_config_json':
            client.create_config_json()

        elif func == 'get_health_alive':
            target = sys.argv[2].lower()
            client.get_health_alive(target)

        elif func == 'get_journey_by_id_and_pk':
            target = sys.argv[2].lower()
            id = sys.argv[3]
            pk = sys.argv[4]
            client.get_journey_by_id_and_pk(target, id, pk)

        elif func == 'get_journey_by_pk':
            target = sys.argv[2].lower()
            pk = sys.argv[3]
            client.get_journey_by_pk(target, pk)

        elif func == 'post_journey_relay':
            target = sys.argv[2].lower()
            infile = sys.argv[3]
            if len(sys.argv) > 4:
                pk = sys.argv[4]
            else:
                pk = str(int(time.time()))
            client.post_journey_relay(target, infile, pk)

        elif func == 'delete_all_journey_docs':
            target = sys.argv[2].lower()
            infile = sys.argv[3]
            client.delete_all_journey_docs(target, infile)

        elif func == 'create_aci_config_json':
            client.create_aci_config_json()
    
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')