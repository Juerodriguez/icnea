from ..main.utils import timer_utils
import time


class TestTimer:

    def test_start_timer(self):
        assert int((time.time() + 10)) == int(timer_utils.start_timer(10))

    def test_finish_timer(self):
        assert timer_utils.finish_timer(-1)

