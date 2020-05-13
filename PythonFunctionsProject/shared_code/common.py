import json
import os

import arrow
import azure.functions as func

def app_version():
    return '2020/05/13 08:54'

def now():
    return arrow.utcnow()

def curr_timestamp():
    return arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')

def epoch():
    return arrow.utcnow().timestamp

def env_var(name, default_value):
    if name in os.environ:
        return os.environ[name]
    else:
        return default_value

def write_cosmos_doc(doc_binding, doc_object):
    return doc_binding.set(func.Document.from_json(json.dumps(doc_object)))
