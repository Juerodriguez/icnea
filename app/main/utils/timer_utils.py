import time


def start_timer(seconds):
    start = time.time()
    time_limit = start + seconds
    return time_limit


def finish_timer(time_limit):
    return time.time() >= time_limit
