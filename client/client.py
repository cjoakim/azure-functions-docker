"""
Usage:
  python client.py create_config_json
  python client.py http_load_regions local
  python client.py http_query_by_pk local eastus
  python client.py http_query_by_pk azure germanynorth
  python client.py http_query_by_geo local 8.806422 53.073635 10
  python client.py http_query_by_geo azure -78.3889 36.6681 200
  python client.py http_query_by_pk azure event-eastasia
  python client.py send_events_to_hub data/20190317-asheville-marathon-events.json 5000
"""

# Python HTTP Client program for this Azure Function.
# Chris Joakim, Microsoft, 2020/05/15
#
# https://pypi.org/project/azure-eventhub/#publish-events-to-an-event-hub

import json
import os
import sys
import time
import traceback
import uuid 

import arrow
import requests

from docopt import docopt

from azure.eventhub import EventHubProducerClient, EventData

VERSION = 'v20200515a'


class Client:

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

    def http_load_regions(self, target):
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

    def http_query_by_pk(self, target, pk):
        url = self.config[target]
        print('url: {}'.format(url))
        data = dict()
        data['query'] = "select * from c where c.pk = '{}'".format(pk)
        self.execute_post(url, data, {})

    def http_query_by_geo(self, target, lng, lat, meters):
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

    def send_events_to_hub(self, infile, max_count):
        print('send_events_to_hub; infile: {} max_count: {}'.format(infile, max_count))

        conn_str = os.environ['AZURE_EVENTHUB_CONN_STRING']
        hub_name = os.environ['AZURE_EVENTHUB_HUBNAME']
        # print('conn_str: {}'.format(conn_str))
        # print('hub_name: {}'.format(hub_name))

        producer_client = EventHubProducerClient.from_connection_string(conn_str, eventhub_name=hub_name)
        print('producer_client: {}'.format(producer_client))

        lines = self.read_lines(infile)
        with producer_client:
            for line_idx, line in enumerate(lines):
                if line_idx < max_count:
                    event = json.loads(line)
                    now = arrow.utcnow()
                    event['pk'] = event['name']
                    event['sent_time'] = str(now)
                    event['sent_epoch'] = now.timestamp
                    msg = json.dumps(event)
                    try:
                        event_data_batch = producer_client.create_batch()
                        event_data_batch.add(EventData(msg))
                        producer_client.send_batch(event_data_batch)
                        print('sent: {}'.format(msg))
                    except:
                        traceback.print_exc(file=sys.stdout)

    def read_lines(self, infile):
        lines = list()
        with open(infile, 'rt') as f:
            for line in f:
                lines.append(line)
        return lines

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
        client = Client()

        if func == 'create_config_json':
            client.create_config_json()

        elif func == 'http_load_regions':
            target = sys.argv[2].lower()
            client.http_load_regions(target)

        elif func == 'http_query_by_pk':
            target, pk = sys.argv[2].lower(), sys.argv[3]
            client.http_query_by_pk(target, pk)

        elif func == 'http_query_by_geo':
            target = sys.argv[2].lower()
            lat = float(sys.argv[3].lower())
            lng = float(sys.argv[4].lower())
            km  = int(sys.argv[5].lower())
            client.http_query_by_geo(target, str(lat), str(lng), str(km * 1000))
        elif func == 'send_events_to_hub':
            infile = sys.argv[2]
            max_count = int(sys.argv[3])
            client.send_events_to_hub(infile, max_count)
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')