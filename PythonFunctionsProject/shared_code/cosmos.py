__author__ = 'Chris Joakim'

import json
import os

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import azure.cosmos.documents as documents

# pip install azure-cosmos
# https://pypi.org/project/azure-cosmos/
# https://github.com/Azure/azure-cosmos-python
# https://docs.microsoft.com/bs-latn-ba/azure/cosmos-db/sql-api-python-samples
# https://github.com/Azure/azure-cosmos-python/blob/master/samples/CollectionManagement/Program.py


class Cosmos(object):

    def __init__(self, opts):
        self._opts = opts
        self._dbname = None
        self._cname = None
        print(self._opts)
        uri = opts['uri']
        key = opts['key']
        self._client = cosmos_client.CosmosClient(uri, {'masterKey': key})
        print(self._client)

    def list_databases(self):
        return list(self._client.ReadDatabases())

    def list_containers(self, dbname):
        link = self.db_link(dbname)
        return list(self._client.ReadContainers(link))

    def set_db(self, dbname):
        dlink = self.db_link(dbname)
        self._dbname = dbname
        try:
            self._client.CreateDatabase({'id': dbname})
            return self._client.ReadDatabase(dlink)
        except errors.HTTPFailure:
            return self._client.ReadDatabase(dlink)

    def create_container(self, dbname, cname, pk, throughput):
        clink = self.container_link(dbname, cname)
        pk_spec = dict()
        pk_spec['paths'] = [pk]
        pk_spec['kind'] = documents.PartitionKind.Hash
        con_spec = dict()
        con_spec['id'] = cname
        con_spec['partitionKey'] = pk_spec
        #print(json.dumps(con_spec, sort_keys=False, indent=2))
        try:
            dlink = self.db_link(dbname)
            return self._client.CreateContainer(
                dlink, con_spec, {'offerThroughput': throughput})
        except:
            return None

    def get_container(self, dbname, cname):
        clink = self.container_link(dbname, cname)
        print('get_container; clink: {}'.format(clink))
        return self._client.ReadContainer(clink)

    def update_container_throughput(self, dbname, cname, throughput):
        try:
            offer = self.get_container_offer(dbname, cname)
            curr_throughput = offer['content']['offerThroughput']
            offer['content']['offerThroughput'] = abs(int(throughput))
            self._client.ReplaceOffer(offer['_self'], offer)
            # print('update_container_throughput: {} {} {} -> {}'.format(
            #     dbname, cname, curr_throughput, throughput))
            return throughput
        except errors.HTTPFailure:
            return -1

    def get_container_offer(self, dbname, cname):
        try:
            con = self.get_container(dbname, cname)
            sql = "select * from root r where r.offerResourceId='{}'".format(con['_rid'])
            #print(sql)  select * from root r where r.offerResourceId='YtUbAIrmgx4='
            offers = list(self._client.QueryOffers(sql))
            return offers[0]
        except errors.HTTPFailure:
            return -1

    def upsert_doc(self, dbname, cname, doc):
        try:
            clink = self.container_link(dbname, cname)
            return self._client.UpsertItem(clink, doc)
        except errors.HTTPFailure:
            return None

    def delete_doc(self, dbname, cname, doc, pkattr):
        try:
            link = self.doc_link(dbname, cname, doc['id'])
            return self._client.DeleteItem(link, {'partitionKey': doc[pkattr]})
        except errors.HTTPFailure:
            return None

    def query_container(self, dbname, cname, sql, xpartition):
        try:
            clink = self.container_link(dbname, cname)
            return self._client.QueryItems(
                clink, sql, {'enableCrossPartitionQuery': xpartition})
        except errors.HTTPFailure:
            return None

    # primarily private methods below

    def db_link(self, dbname):
        return 'dbs/{}'.format(dbname)

    def container_link(self, dbname, cname):
        return 'dbs/{}/colls/{}'.format(dbname, cname)

    def doc_link(self, dbname, cname, docid):
        return 'dbs/{}/colls/{}/docs/{}'.format(dbname, cname, docid)

    def last_request_charge(self):
        return self._client.last_response_headers['x-ms-request-charge']

    def last_response_headers(self):
        return self._client.last_response_headers

    def client(self):
        return self._client
