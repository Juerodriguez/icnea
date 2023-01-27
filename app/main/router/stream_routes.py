import cv2
from fastapi import APIRouter, Request
from ..services import inference
from fastapi.responses import StreamingResponse
from ..config import Settings
from fastapi.templating import Jinja2Templates
import time

config = Settings()
router = APIRouter(prefix="/stream", tags=["Video Stream"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })


@router.get("/get_video", response_class=StreamingResponse)
async def video_stream():
    inicio = time.time()
    response = StreamingResponse(get_image(), media_type="multipart/x-mixed-replace;boundary=frame")
    fin = time.time()
    print(fin - inicio)
    return response


def get_image():
    cap = cv2.VideoCapture("/home/stylorj/PycharmProjects/JUGO/icneaproject/icnea/28Nov.webm")
    model = f"{config.MODEL_PATH}/best.onnx"  # Cambiar al nombre del modelo que quiere probar
    classesfile = config.CLASSES_PATH
    with open(classesfile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    net = cv2.dnn.readNetFromONNX(model)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    while True:
        ret, frame = cap.read()
        output = inference.inference(net, frame, classes)
        # asyncio.create_task(generate_remaining_models(model, frame))
        if output is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", output)
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
