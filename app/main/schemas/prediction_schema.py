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
    id: str = Field(default_factory=generate_uuid)
    frame: List[Frame]


