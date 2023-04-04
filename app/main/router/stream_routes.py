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
router_stream = APIRouter(prefix="/stream", tags=["Video Stream"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router_stream.get("/test")
async def read_root(request: Request):
    """
    Endpoint for test Stream result.

    :param request:
    :return:
    """
    return templates.TemplateResponse("video.html", {
        "request": request
    })


@router_stream.get("/get_video", response_class=StreamingResponse)
async def video_stream() -> StreamingResponse:
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
    frames_to_redis = []

    model = f"{config.MODEL_PATH}/best43v8s.onnx"  # Cambiar al nombre del modelo que quiere probar
    classesfile = config.CLASSES_PATH
    with open(classesfile, 'rt') as f: # Obtener las clases al predecir
        classes = f.read().rstrip('\n').split('\n')
    # Read the Net model
    net = cv2.dnn.readNetFromONNX(model)
    # Set CUDA Backend
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # -------- Get video --------
    # Using webcam
    #cap = cv2.VideoCapture(0)
    # Using UDP
    cap = cv2.VideoCapture("udp://192.168.0.101:8080?overrun_nonfatal")
    # Using RSTP
    
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    while True:
        ret, frame = cap.read()

        if ret:
            # Save the number of frames each 10 seconds
            num_frames += 1
            if timer2.flag1:
                timer2.timer_limit_start_save = start_timer(5)
                timer2.flag1 = False
            if finish_timer(timer2.timer_limit_start_save):
                timer2.flag1 = True
                redis_client_service.save_cache(FramesCount(frames_count=num_frames))
                num_frames = 0
            # Call the inference service to object detection

            task = asyncio.create_task(inference_service.inference(net, frame, classes, timer1, frames_to_redis))
            output = await task

            if output is None:
                continue
            # Encode the frame to stream it.
            (flag, encodedImage) = cv2.imencode(".jpg", output)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
