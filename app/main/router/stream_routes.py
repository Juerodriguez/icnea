import cv2
from fastapi import APIRouter, Request
from ..services import inference_service, redis_client_service
from fastapi.responses import StreamingResponse
from ..config import Settings
from fastapi.templating import Jinja2Templates
import time
import asyncio
from ..schemas.timer_schema import Timer
from ..schemas.prediction_schema import FramesCount
from ..utils.timer_utils import start_timer, finish_timer

config = Settings()
router = APIRouter(prefix="/stream", tags=["Video Stream"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router.get("/test")
async def read_root(request: Request):
    """
    Endpoint for test Stream result.

    :param request:
    :return:
    """
    return templates.TemplateResponse("index.html", {
        "request": request
    })


@router.get("/get_video", response_class=StreamingResponse)
async def video_stream():
    """
    This endpoint is for Stream the video inference results

    :return:
    """
    return StreamingResponse(get_image(), media_type="multipart/x-mixed-replace;boundary=frame")


async def get_image():
    """
    Funtion for Capture the video stream, set the CUDA Backend and call a loop for inference frame by frame.

    :return:
    """
    timer1 = Timer()
    timer2 = Timer()
    num_frames = 0
    redis_client_service.delete_all_cache()
    model = f"{config.MODEL_PATH}/best.onnx"  # Cambiar al nombre del modelo que quiere probar
    classesfile = config.CLASSES_PATH
    with open(classesfile, 'rt') as f: # Obtener las clases al predecir
        classes = f.read().rstrip('\n').split('\n')

    net = cv2.dnn.readNetFromONNX(model)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)  # Seleccionar cuda para inferir en GPU
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    cap = cv2.VideoCapture("M.mp4")  # udp://192.168.1.49:8080?overrun_nonfatal
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    while True:
        ret, frame = cap.read()

        # output = await inference.inference(net, frame, classes)

        if ret:
            num_frames += 1
            if timer2.flag1:
                timer2.timer_limit_start_save = start_timer(10)
                timer2.flag1 = False
            if finish_timer(timer2.timer_limit_start_save):
                timer2.flag1 = True
                redis_client_service.save_cache(FramesCount(frame_count=num_frames)) #todo probar guardo mostrando resultado en api
                print(num_frames)  # todo print solo para pruebas
                num_frames = 0

            task = asyncio.create_task(inference_service.inference(net, frame, classes, timer1))
            output = await task
            if output is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", output)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
