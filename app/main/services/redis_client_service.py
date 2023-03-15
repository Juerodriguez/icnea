import json
import redis
from typing import Union
from redis.exceptions import ResponseError
from ..schemas.prediction_schema import Prediction, FramesCount, Calibration


redis_client = redis.Redis(host="redis", port=6379)


def save_cache(data: Union[Prediction, FramesCount, Calibration]) -> str:
    try:
        redis_client.set(data.dict()["id"], json.dumps(data.dict()))
        return "Guardado con exito"
    except ResponseError as e:
        print(e)


def delete_all_cache(key) -> str:
    try:
        redis_client.delete(key)
        return "Borrado con exito"
    except ResponseError as e:
        print(e)


def get_all_cache() -> iter:
    try:
        keys_iter = [json.loads(redis_client.get(key)) for key in redis_client.keys()]
        return keys_iter
    except ResponseError as e:
        print(e)
