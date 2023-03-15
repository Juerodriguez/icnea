from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from ..services import redis_client_service, presence_service
from ..config import Settings
from ..schemas.prediction_schema import Calibration
import time
import asyncio

config = Settings()
router_detect = APIRouter(prefix="/detections", tags=["Detections report"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router_detect.get("/get_report")
async def detections_report_get() -> JSONResponse:
    """
    This endpoint serves for produce a report with the presence of objects and their correct position.
    :return:
    """
    comparator_calibration = []
    data = redis_client_service.get_all_cache()
    is_present = {}
    in_position = {}
    for dicts in data:
        if "frame_calibration" in dicts:
            frames = dicts["frame_calibration"]
            for frame in frames:
                comparator_calibration.append(frame["frame"])
    comparator2 = await filter_one_frame_per_label(data)
    if len(comparator_calibration) != len(comparator2):
        return JSONResponse(content={
            "message": "Se requiere calibracion"
        })
    else:
        for i in range(len(comparator_calibration)):
            for key in comparator_calibration[i]["coordinate"]:
                range_max = comparator_calibration[i]["coordinate"][key] * 1.05
                range_min = comparator_calibration[i]["coordinate"][key] * 0.95
                if range_min <= comparator2[i]["coordinate"][key] <= range_max:
                    pass

    return JSONResponse(content={
        "presence": is_present,
        "position": in_position
    })


@router_detect.get("/calibrate_ready")
async def calibrate_ready() -> JSONResponse:
    """
    Endpoint to know if the calibration is ready.
    :return:
    """

    data = redis_client_service.get_all_cache()
    for dicts in data:
        if "frame" in dicts:
            response = {"message": "Listo para calibrar"}
            return JSONResponse(content=response)
    response = {"message": "Faltan datos para calibrar"}
    return JSONResponse(content=response, status_code=204)


@router_detect.get("/calibrate")
async def calibrate_position_objects() -> JSONResponse:
    """
    This endpoint is for calibrate the object position, the coordinate results will be a reference position to determine
    the correct order of objects.
    :return:
    """
    data = redis_client_service.get_all_cache()
    for dicts in data:
        if "frame_calibration" in dicts:
            redis_client_service.delete_all_cache(key="calibration")

    frame_response = await filter_one_frame_per_label(data)
    if frame_response:
        redis_client_service.save_cache(Calibration(frame_calibration=frame_response))
        return JSONResponse(content=frame_response)
    else:
        response = {"message": "Fallo la calibracion"}
        return JSONResponse(content=response, status_code=304)


async def filter_one_frame_per_label(data) -> list:
    """
    Async function to obtain one frame per label found.
    :param data:
    :return:
    """
    for dicts in data:
        if "frame" in dicts:
            is_present = presence_service.presence(data)
            labels = set([key for key, value in is_present.items() if value])
            frames_to_redis = []
            frames = dicts["frame"]
            for frame in frames:
                if frame["label"] in labels:
                    labels.discard(frame["label"])
                    frames_to_redis.append(frame)
            return frames_to_redis
