from pydantic import BaseSettings, BaseModel
import cv2


class Colors(BaseModel):
    BLACK = (0, 0, 0)
    BLUE = (255, 178, 50)
    YELLOW = (0, 255, 255)


class Text(BaseModel):
    FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.7
    THICKNESS = 1


class Constants(BaseModel):
    INPUT_WIDTH = 640
    INPUT_HEIGHT = 640
    SCORE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.45
    CONFIDENCE_THRESHOLD = 0.45


class OpenCV2Config(BaseModel):
    COLORS: Colors
    TEXT_PARAMETERS: Text
    CONSTANTS: Constants


class Settings(BaseSettings):
    MODEL_PATH: str = "./models/"
    CLASSES_PATH: str = "classes.txt"
    OPENCVCONFIG: OpenCV2Config


