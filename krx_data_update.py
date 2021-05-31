import datetime
import json
import os

import coredotfinance.krx as cdf
import krx_crawler

# krx_data_test 는 krx_data 로 바뀌어야 한다. (테스트 이후)
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'krx_data_test')

def get_data(item_name):
    path = os.path.join(DATA_PATH, item_name + '.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# item이 data list에 있는지 확인한다.
def is_new_item(item_name):
    list_dir = os.listdir(DATA_PATH)
    if item_name + '.json' in list_dir:
        return False
    else:
        return True


# 최신 날짜를 받아 온다
def get_latest_date(data, item_name):
    return list(data[item_name]['종가'].keys())[0]


# data 합치기
def merge_data(new_data, data, item_name):
    for key in data[item_name].keys():
        data[item_name][key].update(new_data[item_name][key])
    return data


def get_new_data(data, item_name):
    latest = get_latest_date(data, item_name).replace('-', '')
    today = datetime.datetime.now().isoformat().split('T')[0].replace('-', '')
    return krx_crawler.get_item_data(item_name, latest, today)
