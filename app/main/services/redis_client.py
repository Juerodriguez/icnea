import redis
from redis.exceptions import ResponseError

redis_client = redis.Redis(host=redis, port=6379)


def save_hash(key: str, data: dict):
    try:
        redis_client.hset(name=key, mapping=data)
    except ResponseError as e:
        print(e)


def get_hash(key: str):
    try:
        redis_client.hgetall(name=key)
    except ResponseError as e:
        print(e)


def delete_hash(key: str, keys: list):
    try:
        redis_client.hdel(key, *keys)
    except ResponseError as e:
        print(e)


def get_all():
    try:
        keys = redis_client.keys("*")
        redis_client.hgetall(name=keys)
    except ResponseError as e:
        print(e)
