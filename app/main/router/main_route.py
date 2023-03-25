from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from ..services import redis_client_service, presence_service
from ..config import Settings
from ..schemas.prediction_schema import Calibration
from ..utils import labels_utils


config = Settings()
router_main = APIRouter(prefix="/main", tags=["Principal page"])
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)