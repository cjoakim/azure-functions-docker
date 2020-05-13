import json
import logging as log
import os

import arrow
import azure.functions as func

from ..shared_code import common

def main(req: func.HttpRequest, context: func.Context, doc: func.Out[func.Document]) -> func.HttpResponse:
    fname  = context.function_name
    inv_id = context.invocation_id
    log.info(f'{fname} HTTP trigger, invocation_id: {inv_id}, app_version: {common.app_version()}')

    resp_data = dict()
    resp_data['pk'] = inv_id
    resp_data['function_name'] = fname
    resp_data['invocation_id'] = inv_id
    resp_data['app_version'] = common.app_version()
    resp_data['image_name'] = common.env_var('DOCKER_CUSTOM_IMAGE_NAME', '?')
    resp_data['curr_timestamp'] = common.curr_timestamp()

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
        resp_data['msg'] = f'Hello {name}, the date time is {str(now)}, epoch {epoch}'
        log.info(json.dumps(resp_data))
        common.write_cosmos_doc(doc, resp_data)
        return func.HttpResponse(json.dumps(resp_data, indent=4, sort_keys=False))
    else:
        resp_data['error_msg'] = 'Please pass a name on the query string or in the request body'
        return func.HttpResponse(json.dumps(resp_data, indent=4, sort_keys=False), status_code=400)
