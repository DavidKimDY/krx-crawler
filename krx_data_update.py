import datetime
import json
import os
import sys

import krx_crawler

# krx_data_test 는 krx_data 로 바뀌어야 한다. (테스트 이후)
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "krx_data_test")


def get_data(item_name):
    path = os.path.join(DATA_PATH, item_name + ".json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(item_name, data):
    path = os.path.join(DATA_PATH, item_name + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent="\t")


# item이 data list에 있는지 확인한다.
def is_new_item(item_name):
    list_dir = os.listdir(DATA_PATH)
    if item_name + ".json" in list_dir:
        return False
    else:
        return True


# 최신 날짜를 받아 온다
def get_latest_date(data, item_name):
    return list(data[item_name]["종가"].keys())[0].replace("-", "")


# data 합치기
def merge_data(new_data, data, item_name):
    for key in data[item_name].keys():
        new_data[item_name][key].update(data[item_name][key])
    return new_data


def get_new_data(item_name, latest_date):
    today = datetime.datetime.now().isoformat().split("T")[0].replace("-", "")
    return krx_crawler.get_item_data(item_name, latest_date, today)


def update(item_name):
    if is_new_item(item_name):
        data = None
        latest_date = "00000000"
        pass
    else:
        data = get_data(item_name)
        latest_date = get_latest_date(data, item_name)

    new_data = get_new_data(item_name, latest_date)
    if data is None:
        data = new_data
    else:
        data = merge_data(new_data, data, item_name)
    save_data(item_name, data)


if __name__ == "__main__":
    item_name_ = sys.argv[1]
    if item_name_.endswith('json'):
        update(item_name_.replace('.json', ''))
