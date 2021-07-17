import os
import json

import mongodb_util as mu
import pipeline as ppl

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def get_file_list():
    return os.listdir('data/')


def open_file(file):
    with open(os.path.join(FILE_PATH, 'data', file)) as f:
        return json.load(f)


def get_date(file):
    return file.replace('.json', '')


def is_json(file):
    if file.endswith('.json'):
        return True
    else:
        return False


# 새로 상장된 회사는 insert 한다.
def insert_document(collection, data):
    return # collection.insert_one(data)


def update_document(collection, data, code):
    """
    collection.update(
        {'code': code, 'type': 'stock', 'source': 'krx'},
        {'$push': {
            'data': {
                '$each': [data],
                '$sort': {'날짜': -1}
            }
        }
        }
    )
    """


def tagging_for_krx_storage(data, date):
    return {
        'type': 'price',
        'groupby': 'date',
        'date': date,
        'data': data
    }


def tagging_for_new_data(data, code):
    return {
        'code': code,
        'type': 'stock',
        'source': 'krx',
        'data': data
    }


def is_new_data(collection, code):
    if collection.count_documents({'code': code, 'type': 'stock', 'source': 'krx'}) == 0:
        return True
    else:
        return False


def make_storage_dir():
    if not os.path.isdir('storage'):
        os.mkdir('storage')


# mdb에 보내진 파일은 temp_storage에 저장
def mv_data_to_temp(file_name):
    os.system(f'mv data/{file_name} storage/{file_name}')


def insert(data, collection, date):
    map_ = {
        '종목명': 'name',
        '시장구분': 'market',
        '소속부': 'division',
        '종가': 'close',
        '대비': 'change',
        '등락률': 'change_ratio',
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '거래량': 'trading_volume',
        '거래대금': 'trading_value',
        '시가총액': 'market_cap',
        '상장주식수': 'shares_outstanding',
        '날짜': 'date'
    }

    document = {'symbol': data['종목코드']}
    del data['종목코드']

    for key in data.keys():
        new_key = map_[key]
        value = data[key]
        document[new_key] = value
    document['date'] = date
    collection.insert_one(document)


def main():
    make_storage_dir()
    krx_stock_collection = mu.get_mongodb_collection('krx_stock')
    krx_storage_collection = mu.get_mongodb_collection('krx_storage')
    file_list = get_file_list()

    for file in file_list:
        print(file)
        raw_data = open_file(file)
        date = get_date(file)
        data_for_krx_storage = tagging_for_krx_storage(raw_data, date)
        insert_document(krx_storage_collection, data_for_krx_storage)
        data_list = ppl.convert(raw_data)

        for data in data_list:
            insert(data, krx_stock_collection, date)

        mv_data_to_temp(file)


if __name__ == '__main__':
    main()
