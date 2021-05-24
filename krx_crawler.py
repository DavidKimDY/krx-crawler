import pickle
import json
import asyncio
from time import time

import pandas as pd
import coredotfinance as cdf


def get_item_list():
    return cdf.get()["종목명"]


def get_item_gen():
    return (item for item in cdf.get()['종목명'])


def df2json(df):
    return eval(df.to_json())


def item_code2index(df):
    df.index = df["종목코드"]
    df.drop(["종목코드"], axis="columns", inplace=True)
    return df


def get_item_data(item_name):
    data = cdf.get(item_name, "00000000", "99999999")
	if '종목명' in data.columns:
		data.drop('종목명', axis='columns', inplace=True)
    # datetime to string in order for df.index to convert to json properly
    data.index = [indx.isoformat().split("T")[0] for indx in data.index]
    data_json = df2json(data)
    print(item_name)
    return {item_name: data_json}


def get_ip(file):
    with open(file, "rb") as f:
        return pickle.load(f)


def has_next(gen):
    try:
        return next(gen)
    except StopIteration:
        return 'No element'


async def crawler_test(item_gen):
    loop = asyncio.get_event_loop()
    tasks = []
    count = 0
    stop_sign = False
    while count < 100: # test 원래는 100개 계획
        item_name = has_next(item_gen)
        if item_name == 'No element':
            stop_sign = True
            break
        task = loop.run_in_executor(None, get_item_data, item_name)
        tasks.append(task)
        count += 1
    result_ = await asyncio.gather(*tasks)
    return result_, stop_sign


if __name__ == "__main__":
    stop_sign = False
    item_gen = get_item_gen()
    while not stop_sign:
        now = time()
        result, stop_sign = asyncio.run(crawler_test(item_gen))
        for data in result:
            item_name = list(data.keys())[0]
            with open(f"krx_data/{item_name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent="\t")
        print(time() - now)
