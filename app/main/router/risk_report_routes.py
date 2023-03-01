from fastapi import APIRouter, Request
from ..services import redis_client_service
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
        presence_object(data)

        datos = {
            "Coping": False,
            "saw": False,
            "Drill": False,
            "Hammer": False,
            "Pliers": False,
            "Scissors": False,
            "Screwdriver": False,
            "Spanner": False,

        }

    else:
        data = {
            "message": "No se detectaron objetos"
        }


    """for key in data.keys():
        if len(response[key]) > len(num_frames / 2):
            data[key] = True"""

    return data


@router_detect.post("/calibrate")
async def calibrate_position_objects():
    """
    This endpoint is for calibrate the object position, the coordinate results will be a reference position to determine
    the correct order of objects.
    :return:
    """
    pass
