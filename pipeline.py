import json
import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = 'data'
DATA_PATH = os.path.join(FILE_PATH, DATA_DIR)


def get_data(file_name):
    path = os.path.join(DATA_PATH, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_date(file_name):
    return file_name.replace('.json', '')


def get_indices(data):
    return list(data['종목코드'].keys())


def data_by_index(data, index):
    dbi = {}
    for key in data.keys():
        data_by_key = data[key]
        dbi[key] = data_by_key[index]
    return dbi


def add_date(dbi, date):
    dbi['날짜'] = date
    return dbi


def convert(data):
    indices = get_indices(data)
    dbi_list = []
    for index in indices:
        dbi_list.append(data_by_index(data, index))
    return dbi_list


