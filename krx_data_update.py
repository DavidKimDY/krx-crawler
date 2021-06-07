import datetime
import json
import os
import sys
import requests

import mongodb_util as mu
import status_log
from coredotfinance import krx


# delete 는 krx_data 로 바뀌어야 한다. (테스트 이후)
# DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "krx_data")
DATA_DIR = 'krx_data'
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATA_DIR)
STATUS_LOG_PTAH = ''


def save_data(stock_code, data):
    path = os.path.join(DATA_PATH, stock_code + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent="\t")


def get_status_log():
    with open(STATUS_LOG_PTAH, 'r') as f:
        return json.load(f)


# item이 data list(status.json)에 있는지 확인한다.
def is_new_item(collection, stock_code):
    if collection.find({'type': 'status', 'code': stock_code}).count() == 0:
        return True
    else:
        return False


# True면 이미 받은 파일이다.
def is_in_data_dir(stock_code):
    file = stock_code + '.json'
    return file in os.listdir(DATA_DIR)


def get_date_list(data, name):
    return list(data[name]['종가'].keys())


def get_item_list(data, name):
    return list(data[name].keys())


def get_price_data_list(data, name):
    data_dict = data[name]
    data_list = []
    date_list = get_date_list(data, name)
    item_list = get_item_list(data, name)

    for date in date_list:
        data_ = {'날짜': date}
        for item in item_list:
            if item == '종목명':
                continue
            data_[item] = data_dict[item][date]
        data_list.append(data_)
    return data_list


# 상장 회사명이 달라지는 경우는?
def transform_data_for_mdb(data, stock_code, stock_name):
    stock_price_data = get_price_data_list(data, stock_name)
    return {
        'name': stock_name,
        'code': stock_code,
        'type': 'price',
        'data': stock_price_data
    }


# 최신 날짜 +1 일 해준다.
def add_1_day(latest_date):
    res = datetime.datetime.strptime(latest_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    return str(res.date())


# update를 시작해야 되는 날을 리턴한다
def get_start_date(status):
    latest_data = status_log.get_last_updated_date(status)
    return add_1_day(latest_data).replace('-', '')


def df2json(df):
    return eval(df.to_json())


def get_item_data(stock_name, start_date, today):
    data = krx.get(stock_name, start_date, today)
    if "종목명" in data.columns:
        data.drop("종목명", axis="columns", inplace=True)
    # datetime to string in order for df.index to convert to json properly
    data.index = [indx.isoformat().split("T")[0] for indx in data.index]
    data_json = df2json(data)
    print(stock_name)
    return {stock_name: data_json}


def is_already_updated(status, stock_code):
    if is_in_data_dir(stock_code):
        return True
    latest_date = status_log.get_last_updated_date(status)
    today = str(datetime.datetime.now().date())
    if today == latest_date:
        return True
    else:
        return False


# 종목코드 에러 해결후에는 stock_name -> stock_code
def get_date_until_today(stock_name, start_date):
    today = str(datetime.datetime.now().date()).replace("-", "")
    data = get_item_data(stock_name, start_date, today)
    return data


# name_code -> '삼성전자^005930'
def update_data(stock_code, stock_name, start_date):
    print(start_date)
    try:
        data = get_date_until_today(stock_name, start_date)
    except requests.ConnectionError as e:
        print(f'Ip might be blocked\nerror msg: {e}')
        return
    transformed_data = transform_data_for_mdb(data, stock_code, stock_name)
    save_data(stock_code, transformed_data)


def main():
    code_name = sys.argv[1]
    stock_code, stock_name = code_name.split('^')
    collection = mu.get_mongodb_collection()

    if is_new_item(collection, stock_code):
        status_log.update_new_status(collection, stock_code)
        status = status_log.get_status(collection, stock_code)
        start_date = "00000000"
    else:
        status = status_log.get_status(collection, stock_code)
        start_date = get_start_date(status)

    if is_already_updated(status, stock_code):
        print(f'{stock_code} already updated')
        return {'msg': 'already updated'}

    print(stock_name, stock_code, 'start')
    update_data(stock_code, stock_name, start_date)
    status_log.update_status(collection, stock_code)


if __name__ == "__main__":
    main()
