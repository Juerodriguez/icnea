from fastapi import APIRouter, Request
from ..services import redis_client
from ..config import Settings
from fastapi.templating import Jinja2Templates
import time
import asyncio

config = Settings()
router_detect = APIRouter(prefix="/detections", tags=["Detections report"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router_detect.get("/get_all")
async def detections_report_get():
    response = redis_client.get_all_cache()
    # redis_client.delete_all_cache()
    return response

