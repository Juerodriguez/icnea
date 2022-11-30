import cv2
import uvicorn
from fastapi import FastAPI
from inference import inference
from fastapi.responses import StreamingResponse
import config

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.post("/video_stream")
async def video_stream():
    return StreamingResponse(get_image(), media_type="multipart/x-mixed-replace;boundary=frame")


def get_image():
    cap = cv2.VideoCapture(0)
    while True:
        frame = cap.read()
        model = f"{config.MODEL_PATH}YOLOv5s.onnx"  # Cambiar al nombre del modelo que quiere probar
        output = inference.inference(model, frame)
        # asyncio.create_task(generate_remaining_models(model, frame))
        if output is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", output)
        response = (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')
        return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
