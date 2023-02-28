from app.main import create_app
from app.main.router.stream_routes import router
from app.main.router.risk_report_routes import router_detect


app = create_app()
app.include_router(router)
app.include_router(router_detect)
