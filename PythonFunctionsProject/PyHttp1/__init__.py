import logging
import azure.functions as func
import arrow

from ..shared_code import common

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('PyHttp1 HTTP trigger; app_version: {}'.format(common.app_version()))

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
        msg   = 'Hello {}, the date time is {}, epoch {} (common)'.format(name, str(now), epoch)
        logging.info(msg)
        return func.HttpResponse(msg)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400)
