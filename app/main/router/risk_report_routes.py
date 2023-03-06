from fastapi import APIRouter, Request
from ..services import redis_client_service, presence_service
from ..config import Settings
from fastapi.templating import Jinja2Templates
import time
import asyncio

config = Settings()
router_detect = APIRouter(prefix="/detections", tags=["Detections report"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router_detect.get("/get_report")
async def detections_report_get():
    """
    This endpoint serves for produce a report with the presence of objects and their correct position.
    :return:
    """

    data = redis_client_service.get_all_cache()
    if data:
        classes_response = presence_service.presence(data)
    else:
        classes_response = {"message": "No se detectaron objetos"}
    return classes_response


@router_detect.post("/calibrate")
async def calibrate_position_objects():
    """
    This endpoint is for calibrate the object position, the coordinate results will be a reference position to determine
    the correct order of objects.
    :return:
    """
    pass
