from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..config import Settings
from ..utils.calibrate_utils import updateCalibrateStatus, readCalibrateStatus

config = Settings()
router_main = APIRouter(prefix="/main", tags=["Principal page"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)

@router_main.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router_main.get("/mobile", response_class=HTMLResponse)
async def homeMovile(request: Request):
    return templates.TemplateResponse("mobile.html", {"request": request})

@router_main.get("/desktop", response_class=HTMLResponse)
async def homeDesktop(request: Request):
    await updateCalibrateStatus(False)
    return templates.TemplateResponse("desktop.html", {"request": request})