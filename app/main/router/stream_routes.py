import cv2
from fastapi import APIRouter, Request
from ..services import inference
from fastapi.responses import StreamingResponse
from ..config import Settings
from fastapi.templating import Jinja2Templates

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
    return StreamingResponse(get_image(), media_type="multipart/x-mixed-replace;boundary=frame")


def get_image():
    cap = cv2.VideoCapture("/home/stylorj/PycharmProjects/JUGO/icneaproject/icnea/prueba2.mp4")
    model = f"{config.MODEL_PATH}/best.onnx"  # Cambiar al nombre del modelo que quiere probar
    while True:
        ret, frame = cap.read()
        output = inference.inference(model, frame)
        # asyncio.create_task(generate_remaining_models(model, frame))
        if output is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", output)
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
