import os, json
import mongodb_util as mu

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def get_file_list():
    return os.listdir('data/')


def open_file(file):
    with open(os.path.join(FILE_PATH, 'data', file)) as f:
        return json.load(f)


def tagging(data, date):
    return {'type': 'price', 'groupby': 'date', 'date': date, 'data': data}


def get_date(file):
    return file.replace('.json', '')


def is_json(file):
    if file.endswith('.json'):
        return True
    else:
        return False


def main():
    collection = mu.get_mongodb_collection()
    file_list = get_file_list()
    for file in file_list:
        if not is_json(file):
            continue
        data = open_file(file)
        date = get_date(file)
        tagged_data = tagging(data, date)
        collection.insert_one(tagged_data)


if __name__ == '__main__':
    main()
