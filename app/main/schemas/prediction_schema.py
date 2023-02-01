from pydantic import BaseModel, Field
from uuid import uuid4


def generate_uuid():
    return str(uuid4())


class Coordinate(BaseModel):
    left: int
    top: int
    width: int
    height: int


class Prediction(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    coordinate: Coordinate = Coordinate()
    label: str
