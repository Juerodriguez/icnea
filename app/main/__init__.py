from fastapi import FastAPI


def create_app():
    app = FastAPI(title="Icnea Backend")
    return app
