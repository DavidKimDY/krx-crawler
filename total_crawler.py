import sys
import os
import json
import datetime
import time

import coredotfinance.krx as krx

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = 'data'
DATA_PATH = os.path.join(FILE_PATH, DATA_DIR)


def make_8_digit(date):
    return str(date.date()).replace('-', '')


def df2json(df):
    return eval(df.to_json())


def get_item_data(date):
    eight_digit_date = make_8_digit(date)
    df = krx.get('all', eight_digit_date)
    if is_no_data(df):
        return 'no data'
    # datetime to string in order for df.index to convert to json properly
    return df2json(df)


def save_data(date, data):
    date_ = str(date.date())
    path = os.path.join(DATA_PATH, date_ + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent="\t")


def get_date(day):
    start = datetime.datetime(2016, 4, 15)
    return start + datetime.timedelta(days=day)


def is_weekendy(date):
    if date.weekday() == 6 or date.weekday() == 5:
        return True
    else:
        return False


def is_no_data(df):
    if df.isna().sum()['시가총액'] == 0:
        return False
    else:
        return True


def is_end_day(date):
    if date >= datetime.datetime(2021, 6, 10):
        return True
    else:
        return False


def make_dir(directory):
    path = os.path.join(FILE_PATH, directory)
    if not os.path.isdir(path):
        os.mkdir(path)


# day > 0
def main():
    day = int(sys.argv[1])
    make_dir('data')
    date = get_date(day)
    if is_weekend(date):
        make_dir(f'end_{day}')
        print(date, 'Done!!!!!!!!')
        time.sleep(100000)
    if is_sunday(date):
        return
    data = get_item_data(date)
    if data == 'no data':
        return
    save_data(date, data)


if __name__ == '__main__':
    main()
