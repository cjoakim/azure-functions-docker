import json
import logging as log
import os

import arrow
import azure.functions as func

from ..shared_code import common


def main(event: func.EventHubEvent, context: func.Context, doc: func.Out[func.Document]):
    fname = context.function_name
    inv_id = context.invocation_id
    version = common.app_version()
    log.info(f'{fname}, invocation_id: {inv_id}, app_version: {version}')
    body = event.get_body().decode('utf-8')
    log.info('event body type:  %s', str(type(body)))
    log.info('event body data:  %s', body)
    doc.set(func.Document.from_json(body))  # write the event to CosmosDB
