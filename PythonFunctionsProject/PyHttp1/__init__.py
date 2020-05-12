import json
import logging as log
import os

import arrow
import azure.functions as func



from ..shared_code import common

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    fname  = context.function_name
    inv_id = context.invocation_id
    log.info(f'{fname} HTTP trigger, invocation_id: {inv_id}, app_version: {common.app_version()}')

    resp_doc = dict()
    resp_doc['function_name'] = fname
    resp_doc['invocation_id'] = inv_id
    resp_doc['runtime'] = os.environ["FUNCTIONS_WORKER_RUNTIME"]

    name = req.params.get('name')

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        now   = common.now()
        epoch = common.epoch()
        resp_doc['msg'] = f'Hello {name}, the date time is {str(now)}, epoch {epoch}'
        log.info(json.dumps(resp_doc))
        return func.HttpResponse(json.dumps(resp_doc, indent=4, sort_keys=False))
    else:
        resp_doc['error_msg'] = 'Please pass a name on the query string or in the request body'
        return func.HttpResponse(json.dumps(resp_doc, indent=4, sort_keys=False), status_code=400)
