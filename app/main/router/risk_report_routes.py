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

@router_detect.get("/calibrate_ready")
async def calibrate_ready():
    """

    :return:
    """
    data = redis_client_service.get_all_cache()
    for dicts in data:
        if "frame" in dicts:
            return {"message": "Listo para calibrar"}

@router_detect.get("/calibrate")
async def calibrate_position_objects():
    """
    This endpoint is for calibrate the object position, the coordinate results will be a reference position to determine
    the correct order of objects.
    :return:
    """
    data = redis_client_service.get_all_cache()
    is_present = presence_service.presence(data)
    labels = set([key for key, value in is_present.items() if value])
    frames_to_redis = []
    for dicts in data:
        if "frame" in dicts:
            frames = dicts["frame"]
            for frame in frames:
                if frame["label"] in labels:
                    labels.discard(frame["label"])
                    frames_to_redis.append(frame)
    redis_client_service.save_cache_persistent(Prediction(frame=frames_to_redis))

