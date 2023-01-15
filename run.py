from app.main import create_app
from app.main.router.stream_routes import router


app = create_app()
app.include_router(router)
