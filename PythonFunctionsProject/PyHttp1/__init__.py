import logging
import azure.functions as func
import arrow


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        now   = arrow.utcnow()
        epoch = now.timestamp
        msg   = 'Hello {}, the date time is {}, epoch {}'.format(name, str(now), epoch)
        logging.info(msg)
        return func.HttpResponse(msg)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400)
