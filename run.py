from app.main import create_app
from app.main.routes import router
import os

app = create_app(os.getenv("FASTAPI_ENV", "dev"))
app.include_router(router)
