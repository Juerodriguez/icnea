from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from ..services import redis_client_service, presence_service
from ..config import Settings
from ..schemas.prediction_schema import Calibration
from ..utils import labels_utils


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

    positions = 0
    data = redis_client_service.get_all_cache()
    is_present = {}
    in_position = labels_utils.create_dicts_from_labels()

    if data:
        for dicts in data:
            if "frame" in dicts:
                is_present = presence_service.presence(data)
                labels = set([key for key, value in is_present.items() if value])
                if not labels:
                    return JSONResponse(content={
                        "presence": is_present,
                        "position": in_position
                        })
            

    # Obtencion de frames de calibracion que sirven de referencia.
    for dicts in data:
        if "frame_calibration" in dicts:
            frames = dicts["frame_calibration"]
            for frame in frames:
                comparator_calibration.append(frame)

    # Obtencian de un frame por etiqueta en los datos de frames detectados
    comparator_detection = await filter_one_frame_per_label(data)
    # Comparacion entre las posiciones de los frames de calibracion con los detectados
    
    for labels1 in comparator_calibration:
        for labels2 in comparator_detection:
            if labels1["label"] == labels2["label"]:
                positions = 0
                for key in labels1["coordinate"]:
                    range_max = labels1["coordinate"][key] * 1.20
                    range_min = labels1["coordinate"][key] * 0.80
                    if range_min <= labels2["coordinate"][key] <= range_max:
                        positions += 1
                    else:
                        in_position[labels1["label"]] = False
                        # break
                # Si se contabiliza 4 posiciones correctas (left, top, right, height) el objeto esta posicionado.
                if positions == 4:
                    
                    in_position[labels1["label"]] = True

    return JSONResponse(content={
        "presence": is_present,
        "position": in_position
    }, status_code=status.HTTP_200_OK)


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
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    response = {"message": "Faltan datos para calibrar"}
    return JSONResponse(content=response, status_code=status.HTTP_204_NO_CONTENT)


@router_detect.get("/calibrate")
async def calibrate_position_objects() -> JSONResponse:
    """
    This endpoint is for calibrate the object position, the coordinate results will be a reference position to determine
    the correct order of objects.
    :return:
    """
    data = redis_client_service.get_all_cache()
    for dicts in data:
        # Si los datos de calibracion existen en la base de datos estos se deben eliminar para recalibrar.
        if "frame_calibration" in dicts:
            redis_client_service.delete_all_cache(key="calibration")

    frame_response = await filter_one_frame_per_label(data)
    if frame_response:
        redis_client_service.save_cache(Calibration(frame_calibration=frame_response))
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=frame_response)
    else:
        response = {"message": "Fallo la calibracion"}
        return JSONResponse(content=response, status_code=status.HTTP_304_NOT_MODIFIED)


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
