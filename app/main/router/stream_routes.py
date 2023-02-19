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
    return templates.TemplateResponse("index.html", {
        "request": request
    })


@router.get("/get_video", response_class=StreamingResponse)
async def video_stream():
    return StreamingResponse(get_image(), media_type="multipart/x-mixed-replace;boundary=frame")


async def get_image():
    cap = cv2.VideoCapture("28Nov.webm")
    model = f"{config.MODEL_PATH}/best.onnx"  # Cambiar al nombre del modelo que quiere probar
    classesfile = config.CLASSES_PATH
    with open(classesfile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    net = cv2.dnn.readNetFromONNX(model)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    output_layers = net.getUnconnectedOutLayersNames()
    while True:
        ret, frame = cap.read()
        # output = await inference.inference(net, frame, classes)

        if ret:
            ini = time.time()
            task = asyncio.create_task(inference.inference(net, frame, classes, output_layers))
            output = await task
            fin = time.time()
            print(fin - ini)
            if output is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", output)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
