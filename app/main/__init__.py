from fastapi import FastAPI
from .config import config_by_name


def create_app(config_name):
    app = FastAPI()
    # app.config.from_object(config_by_name[config_name])
    return app

