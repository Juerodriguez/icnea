from fastapi import APIRouter, Request
from ..services import redis_client as db
from fastapi.responses import JSONResponse
from ..config import Settings
from fastapi.templating import Jinja2Templates
import time
import asyncio

config = Settings()
router_detect = APIRouter(prefix="/detections", tags=["Detections report"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router_detect.get("/get_all")
async def detections_report_get():
    response = db.get_all()
    return JSONResponse({
        "body": response
    })
