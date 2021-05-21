import pickle
import json
import asyncio
from time import time

import coredotfinance as cdf


def get_item_list():
    return cdf.get()["종목명"]


def df2json(df):
    return eval(df.to_json())


def item_code2index(df):
    df.index = df["종목코드"]
    df.drop(["종목코드"], axis="columns", inplace=True)
    return df


def get_item_data(item_name):
    data = cdf.get(item_name, "00000000", "99999999")
    # datetime to string in order for df.index to convert to json properly
    data.index = [indx.isoformat().split("T")[0] for indx in data.index]
    data_json = df2json(data)
    return {item_name: data_json}


def get_ip(file):
    with open(file, "rb") as f:
        return pickle.load(f)


async def crawler():
    now = time()
    loop = asyncio.get_event_loop()
    tasks = []
    for i in get_item_list():
        task = loop.run_in_executor(None, get_item_data, i)
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    print(time() - now)
    return result


if __name__ == "__main__":
    result = asyncio.run(crawler())
    for i, data in enumerate(result):
        item_name = list(data.keys())[0]
        with open(f"krx_data/{item_name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent="\t")
