from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def create_app():
    app = FastAPI(title="Icnea Backend")
    app.mount("/public", StaticFiles(directory="app/public"), name="public")
    return app