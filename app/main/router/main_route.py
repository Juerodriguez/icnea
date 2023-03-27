from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..config import Settings

config = Settings()
router_main = APIRouter(prefix="/main", tags=["Principal page"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)

@router_main.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main.html", {
        "request": request,
        "message": "get_calibrate_ready()"
    })