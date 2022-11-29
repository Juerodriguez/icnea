import cv2
import uvicorn
from fastapi import FastAPI
import asyncio
from inference import inference
from concurrent.futures import ProcessPoolExecutor
from functools import partial


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.post("/inference")
async def get_image():
    cap = cv2.VideoCapture(0)
    frame = cap.read()
    model = "YOLOv5s.onnx"
    output = inference.inference(model, frame)
    # asyncio.create_task(generate_remaining_models(model, frame))
    # TODO: ENCODE OUTPUT IMAGE
    return output


async def generate_remaining_models(models, image):
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image)
    )


def process_image(models, image):
    for model in models:
        output = inference.inference(model, image)
        return output


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
