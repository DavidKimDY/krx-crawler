import datetime
import os
import json

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = os.path.join(FILE_PATH, 'log')


def get_status(collection, code):
    return collection.find({'type': 'status', 'code': code})[0]


def get_last_updated_date(status):
    return status['last updated']


def update_status(collection, code):
    today = datetime.datetime.now().date()
    if is_before_market_close():
        date = str(today - datetime.timedelta(days=1))
    else:
        date = str(today)
    collection.update({'type': 'status', 'code': code}, {'$set': {'last updated': date}})


# 만약 실행시간이 3시 30분 이전이면...?
def is_before_market_close():
    if datetime.time(15, 30) > datetime.datetime.now().time():
        return True
    else:
        return False


def update_new_status(collection, code):
    collection.insert({'type': 'status', 'code': code, 'last updated': '0000-00-00'})


def make_log_file():
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)


def logging(code, msg, data=None):
    time = str(datetime.datetime.now())
    log_file_path = os.path.join(LOG_DIR, time + '.json')
    log = {
        'code': code,
        'time': time,
        'msg': msg,
        'data': data
    }
    if not os.path.isfile(log_file_path):
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent='\t')


