from environs import Env
from pymongo import MongoClient


def get_env():
    env = Env()
    env.read_env()
    return env


# client를 collection 으로 바꾸어 줄 것을 제안
def get_mongodb_client():
    env = get_env()
    return MongoClient(
        env("HOST"),
        port=int(env("PORT")),
        username=env("USERNAME"),
        password=env("PASSWORD"),
        authSource=env("AUTHSOURCE"),
        authMechanism=env("AUTHMECHANISM")
    )


def get_mongodb_collection(collection):
    client = get_mongodb_client()
    env = get_env()
    return client[env("AUTHSOURCE")][collection]

