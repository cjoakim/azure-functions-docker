import arrow
import os

def app_version():
    return '2020/05/12 05:43'

def now():
    return arrow.utcnow()

def epoch():
    return arrow.utcnow().timestamp

def env_var(name, default_value):
    if name in os.environ:
        return os.environ[name]
    else:
        return default_value
