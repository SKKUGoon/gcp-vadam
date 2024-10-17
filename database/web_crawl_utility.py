from datetime import datetime
import time


class RateLimit:
    def __init__(self, rate_max: int = 999):
        self.num_request = 0
        self.request_start: datetime | None = None
        self.request_end: datetime | None = None
        self.rate_max = rate_max

    def reset(self):
        self.num_request = 0
        self.request_start: datetime | None = None
        self.request_end: datetime | None = None

    def tick(self):
        if self.num_request == 0:
            self.request_start = datetime.now()
        self.num_request += 1

        if self.num_request >= self.rate_max:
            # 1,000 per minute rate limit
            d = datetime.now()
            if (d - self.request_start).seconds >= 60:
                self.reset()
            else:
                print("taking a break...")
                time.sleep(60 - (d - self.request_start).seconds)

