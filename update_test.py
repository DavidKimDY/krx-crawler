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
    return  collection.insert_one(data)

def convert_into_eng_key(data):
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
         '날짜': 'date',
         '종목코드': 'symbol'
         }
    new_data_dict = {}
    for key in data:
        eng_key = map_[key]
        value = data[key]
        new_data_dict[eng_key] = value
    return new_data_dict

def update(data, collection, symbol):
    collection.update(
        {'symbol': symbol},
        {'$push': {
            'data': {
                '$each': [data],
                '$sort': {'date': -1}
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


def is_new_data(collection, symbol):
    if collection.count_documents({'symbol': symbol}) == 0:
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
    data['date'] = date
    collection.insert_one(data)



def main():
    # test only
    # make_storage_dir()
    krx_stock  = mu.get_mongodb_collection('test_krx_stock')
    krx_stock_date = mu.get_mongodb_collection('test_krx_stock_date')
    krx_stock_all  = mu.get_mongodb_collection('test_krx_stock_all')
    file_list = get_file_list()

    for file in file_list:
        print(file)
        raw_data = open_file(file)
        eng_key_data = convert_into_eng_key(raw_data)
        # insert 에서는 documnet['date'] = date 만 있으면 되고
        # insert_document 에서도 그냥 변환없이 바로 넣어 줄 수 있다.
        date = get_date(file)
        data_for_krx_storage = tagging_for_krx_storage(eng_key_data, date)
        insert_document(krx_stock_date, data_for_krx_storage)
        data_list = ppl.convert(eng_key_data)

        for data in data_list:
            insert(data, krx_stock, date)
            symbol = data['symbol']

            if is_new_data(krx_stock_all, symbol):
                insert({'symbol': symbol, 'data': data}, krx_stock_all, date)
            else:
                update(data, krx_stock_all, symbol)

        # test only
        # mv_data_to_temp(file)

if __name__ == '__main__':
    main()
