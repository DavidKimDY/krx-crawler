import json
import os
import datetime

import mongodb_util as mu
import coredotfinance.krx as krx

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = 'data'
DATA_PATH = os.path.join(FILE_PATH, DATA_DIR)


def get_status():
    collection = mu.get_mongodb_collection('krx')
    return collection.find_one({'type': 'status'})


def update_status(date_str):
    collection = mu.get_mongodb_collection('krx')
    collection.update_one({'type': 'status'}, {'$set': {'date': date_str}})


def get_date(status):
    return status['date']


def make_8_digit(date_str):
    return date_str.replace('-', '')


def df2json(df):
    return eval(df.to_json())


def get_item_data(date_str):
    eight_digit_date = make_8_digit(date_str)
    df = krx.get('all', eight_digit_date)
    if is_no_data(df):
        return 'no data'
    # datetime to string in order for df.index to convert to json properly
    return df2json(df)


def save_data(date_str, data):
    path = os.path.join(DATA_PATH, date_str + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent="\t")


def is_weekend(date_str):
    date = str2datetime(date_str)
    if date.weekday() == 6 or date.weekday() == 5:
        return True
    else:
        return False


def is_no_data(df):
    if df.isna().sum()['시가총액'] == 0:
        return False
    else:
        return True


def is_end_day(date_str):
    next_date = datetime.datetime.now() + datetime.timedelta(days=1)
    end_day = str(next_date.date())
    if date_str == end_day:
        return True
    else:
        return False


def str2datetime(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')


def make_dir(directory):
    path = os.path.join(FILE_PATH, directory)
    if not os.path.isdir(path):
        os.mkdir(path)


def add_one_day(date_str):
    print(date_str)
    date = str2datetime(date_str)
    next_day = date + datetime.timedelta(days=1)
    print(next_day)
    return str(next_day.date())


# day > 0
def main():
    make_dir('data')
    status = get_status()
    date_str = get_date(status)
    while not is_end_day(date_str):
        print(date_str)
        date_str = add_one_day(date_str)
        if is_weekend(date_str):
            continue
        data = get_item_data(date_str)
        if data == 'no data':
            continue
        save_data(date_str, data)
        update_status(date_str)


if __name__ == '__main__':
    main()
