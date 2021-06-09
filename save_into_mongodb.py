import json
import os
from datetime import datetime

import mongodb_util as mu
import status_log as sl

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(FILE_PATH, "krx_data")

now = datetime.now()
TODAY_DATE = str(now.date())


def get_file_list():
    data_list = []
    for file_name in os.listdir(DATA_PATH):
        if file_name.endswith('json'):
            data_list.append(file_name)
    return data_list


def get_data(file_name):
    data_file_path = os.path.join(DATA_PATH, file_name)
    with open(data_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_file_name(file_name):
    return file_name.replace('.json', '')


# 기존의 데이터가 있을때 업데이트를 할 수 있다..
# 새 데이터가 들어왔을 때는 다른 방법을 사용해야 한다
def update_document(collection, data):
    code = data['code']
    print(code, data['name'])
    collection.update(
        {'code': code, 'type': 'price'},
        {'$push': {
            'data': {
                '$each': data['data'],
                '$sort': {'날짜': -1}
            }
        }
        }
    )


# 새로 상장된 회사는 insert 한다.
def insert_mongo(collection, data):
    return collection.insert(data)


def is_new_data(collection, daily_data):
    code = daily_data['code']
    # 1인 이유는 status 코드가 있기 때문이다.
    if collection.count_documents({'code': code, 'type': 'price'}) == 0:
        return True
    else:
        return False


def make_daily_temp_dir():
    if not os.path.isdir(f'temp_storage/{TODAY_DATE}'):
        os.system(f'mkdir temp_storage/{TODAY_DATE}')


# mdb에 보내진 파일은 temp_storage에 저장
def mv_data_to_temp(file_name):
    os.system(f'mv krx_data/{file_name} temp_storage/{TODAY_DATE}/{file_name}')


def main():
    make_daily_temp_dir()
    collection = mu.get_mongodb_collection()
    file_list = get_file_list()

    for file_name in file_list:
        print(file_name)
        data = get_data(file_name)

        if is_new_data(collection, data):
            logging_data = insert_mongo(collection, data)
            sl.logging(data['code'], 'inserted in mongodb', data=logging_data)
        else:
            update_document(collection, data)
            sl.logging(data['code'], 'updated in mongodb')
        make_daily_temp_dir()
        mv_data_to_temp(file_name)


if __name__ == '__main__':
    main()
