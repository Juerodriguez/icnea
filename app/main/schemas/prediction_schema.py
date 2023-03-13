from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4


def generate_uuid():
    return str(uuid4())


class Coordinate(BaseModel):
    left: int = None
    top: int = None
    width: int = None
    height: int = None


class Frame(BaseModel):
    coordinate: Coordinate = Coordinate()
    label: str = None


class Prediction(BaseModel):
    id: str = "prediction"
    frame: List[Frame]


class FramesCount(BaseModel):
    id: str = "frames"
    frames_count: int = 0
