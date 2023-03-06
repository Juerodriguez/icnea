import time


def start_timer(seconds: int) -> float:
    start = time.time()
    time_limit = start + seconds
    return time_limit


def finish_timer(time_limit: float) -> bool:
    return time.time() >= time_limit

