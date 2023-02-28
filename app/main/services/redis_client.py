import json
import redis
from redis.exceptions import ResponseError
from ..schemas.prediction_schema import Prediction


redis_client = redis.Redis(host="redis", port=6379)


def save_cache(data: Prediction) -> str:
    try:
        redis_client.set(data.dict()["id"], json.dumps(data.dict()))
        return "Guardado con exito"
    except ResponseError as e:
        print(e)


def delete_all_cache() -> str:
    try:
        # keys_iter = (redis_client.delete(key) for key in redis_client.keys())
        redis_client.flushall()
        return "Borrado con exito"
    except ResponseError as e:
        print(e)


def get_all_cache() -> iter:
    try:
        keys_iter = [json.loads(redis_client.get(key)) for key in redis_client.keys()]
        return keys_iter
    except ResponseError as e:
        print(e)
