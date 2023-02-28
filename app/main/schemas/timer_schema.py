from pydantic import BaseModel
from ..utils.timer_utils import start_timer


class Timer(BaseModel):
    flag1: bool = True
    flag2: bool = True
    timer_limit_start_save: float = start_timer(100)
    timer_limit_end_save: float = start_timer(100)
