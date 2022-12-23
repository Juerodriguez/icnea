from app.main import create_app
import os

app = create_app(os.getenv("FASTAPI_ENV", "dev"))
