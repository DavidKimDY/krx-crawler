import datetime


def get_status(collection, code):
    return collection.find({'type': 'status', 'code': code})[0]


def get_last_updated_date(status):
    return status['last updated']


def update_status(collection, code):
    today = str(datetime.datetime.now().date())
    collection.update({'type': 'status', 'code': code}, {'$set': {'last updated': today}})


def update_new_status(collection, code):
    collection.insert({'type': 'status', 'code': code, 'last updated': '0000-00-00'})
