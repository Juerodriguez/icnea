import cv2
from fastapi import APIRouter, Request
from ..services import inference
from fastapi.responses import StreamingResponse
from ..config import Settings
from fastapi.templating import Jinja2Templates
import time
import asyncio

config = Settings()
router = APIRouter(prefix="/stream", tags=["Video Stream"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router.get("/")
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
    cap = cv2.VideoCapture("M.mp4")
    model = f"{config.MODEL_PATH}/best.onnx"  # Cambiar al nombre del modelo que quiere probar
    classesfile = config.CLASSES_PATH
    with open(classesfile, 'rt') as f: # Obtener las clases al predecir
        classes = f.read().rstrip('\n').split('\n')

    net = cv2.dnn.readNetFromONNX(model)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) # Seleccionar cuda para inferir en GPU
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    while True:
        ret, frame = cap.read()
        # output = await inference.inference(net, frame, classes)

        if ret:

            task = asyncio.create_task(inference.inference(net, frame, classes))
            output = await task
            if output is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", output)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
