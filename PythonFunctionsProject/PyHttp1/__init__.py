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

    response_obj = dict()
    response_obj['function_name'] = fname
    response_obj['invocation_id'] = inv_id
    response_obj['app_version'] = version

    post_data = req.get_json()  # get_json() returns an object (i.e.- dict), not a str
    post_datatype = str(type(post_data))
    log.info(f"post_datatype: {post_datatype}\n{post_data}")

    if 'query' in post_data:
        opts = dict()
        opts['uri'] = common.env_var('AZURE_COSMOSDB_SQLDB_URI', 'none')
        opts['key'] = common.env_var('AZURE_COSMOSDB_SQLDB_KEY', 'none')
        c = cosmos.Cosmos(opts)
        sql = post_data['query']
        items = c.query_container('dev', 'airports', sql, True)
        array = list()
        for item in items:
            print(item)
            array.append(item)
        return func.HttpResponse(json.dumps(array, indent=4, sort_keys=False))
    else:
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


    # if pk:
    #     # Query CosmosDB for Documents with the given pk
    #     opts = dict()
    #     opts['uri'] = common.env_var('AZURE_COSMOSDB_SQLDB_URI', 'none')
    #     opts['key'] = common.env_var('AZURE_COSMOSDB_SQLDB_KEY', 'none')
    #     c = cosmos.Cosmos(opts)
    #     sql = "select * from c where c.pk ='{}'".format(pk)
    #     items = c.query_container('dev', 'airports', sql, True)
    #     array = list()
    #     for item in items:
    #         print(item)
    #         array.append(item)
    #     return func.HttpResponse(json.dumps(array, indent=4, sort_keys=False))
    # else:
    #     post_data = req.get_json()  # get_json() returns an object (i.e.- dict), not a str
    #     post_datatype = str(type(post_data))
    #     log.info(f"post_datatype: {post_datatype}\n{post_data}")

    #     post_data['function_name'] = fname
    #     post_data['invocation_id'] = inv_id
    #     post_data['app_version'] = common.app_version()
    #     post_data['inserted_timestamp'] = common.curr_timestamp()
    #     post_data['inserted_epoch'] = common.epoch()

    #     jstr = json.dumps(post_data, indent=4, sort_keys=False)
    #     log.info(f"writing doc:\n{jstr}")
    #     common.write_cosmos_doc(doc, post_data)
    #     return func.HttpResponse(jstr)

# AZURE_COSMOSDB_SQLDB_URI
# AZURE_COSMOSDB_SQLDB_KEY
# pk = req.params.get('pk')