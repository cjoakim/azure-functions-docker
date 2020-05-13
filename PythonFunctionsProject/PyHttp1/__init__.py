import json
import logging as log
import os

import arrow
import azure.functions as func

from ..shared_code import common
from ..shared_code import cosmos

def main(req: func.HttpRequest, context: func.Context, doc: func.Out[func.Document]) -> func.HttpResponse:
    fname = context.function_name
    inv_id = context.invocation_id
    version = common.app_version()
    log.info(f'{fname}, invocation_id: {inv_id}, app_version: {version}')
    # pk = req.params.get('pk')  # this Function does not use GET requests

    response_obj = dict()
    response_obj['function_name'] = fname
    response_obj['invocation_id'] = inv_id
    response_obj['app_version'] = version

    post_data = req.get_json()  # get_json() returns an object (i.e.- dict), not a str
    post_datatype = str(type(post_data))
    log.info(f"post_datatype: {post_datatype}\n{post_data}")

    if 'query' in post_data:
        # This branch queries the DB using the CosmosDB SDK rather than the Function bindings.
        opts = dict()
        opts['uri'] = common.env_var('AZURE_COSMOSDB_SQLDB_URI', 'none')
        opts['key'] = common.env_var('AZURE_COSMOSDB_SQLDB_KEY', 'none')
        c = cosmos.Cosmos(opts)
        sql = post_data['query']
        response_obj['query'] = sql
        items = c.query_container('dev', 'pyfunction', sql, True)
        response_obj['documents'] = list()
        for item in items:
            print(item)
            response_obj['documents'].append(item)
        response_obj['documents_count'] = len(response_obj['documents'])
        response_obj['last_request_charge'] = c.last_request_charge()
        response_obj['last_response_headers'] = c.last_response_headers()
        return func.HttpResponse(json.dumps(response_obj, indent=4, sort_keys=False))
    else:
        # This branch inserts the given document into the DB via the 'doc' Function bindings.
        post_data['function_name'] = fname
        post_data['invocation_id'] = inv_id
        post_data['app_version'] = common.app_version()
        post_data['inserted_timestamp'] = common.curr_timestamp()
        post_data['inserted_epoch'] = common.epoch()
        common.write_cosmos_doc(doc, post_data)
        response_obj['post_data'] = post_data
        jstr = json.dumps(response_obj, indent=4, sort_keys=False)
        log.info(jstr)
        return func.HttpResponse(jstr)
