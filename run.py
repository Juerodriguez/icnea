from app.main import create_app
from app.main.router.stream_routes import router_stream
from app.main.router.risk_report_routes import router_detect
from app.main.router.main_route import router_main


app = create_app()
app.include_router(router_stream)
app.include_router(router_detect)
app.include_router(router_main)