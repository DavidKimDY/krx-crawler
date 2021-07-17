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
    return collection.insert_one(data)


def update_document(collection, data, code):
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


def main():
    make_storage_dir()
    krx_collection = mu.get_mongodb_collection('krx')
    krx_storage_collection = mu.get_mongodb_collection('krx_storage')
    file_list = get_file_list()

    for file in file_list:
        print(file)
        raw_data = open_file(file)
        date = get_date(file)
        data_for_krx_storage = tagging_for_krx_storage(raw_data, date)
        # print('dfks : ', data_for_krx_storage.keys())
        insert_document(krx_storage_collection, data_for_krx_storage)

        data_list = ppl.convert(raw_data)
        for data in data_list:
            code = data.pop('종목코드')
            data['날짜'] = date
            if is_new_data(krx_collection, code):
                print(code, 'is new')
                new_data = tagging_for_new_data(data, code)
                insert_document(krx_collection, new_data)
            else:
                print(code, 'is updated', file)
                update_document(krx_collection, data, code)
        mv_data_to_temp(file)


if __name__ == '__main__':
    main()
