import arrow

def app_version():
    return '2020/05/12 05:43'

def now():
    return arrow.utcnow()

def epoch():
    return arrow.utcnow().timestamp
