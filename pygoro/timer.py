from typing import Optional
import time

from pygoro.channel import Channel
from pygoro.goroutine import go


class Timer:
    time: float
    counter: int
    interval: bool
    channel: Channel

    def __init__(self, time: float, interval: Optional[bool] = False) -> None:
        self.time = time
        self.counter = 0
        self.interval = interval
        self.channel = Channel()
        go(self.wait())

    def wait(self):
        timeend = time.time() + self.time
        while not self.channel.closed:
            if time.time() >= timeend:
                break
        if not self.channel.closed:
            self.finish()

        yield
    
    def finish(self):
        self.channel << self.counter
        self.counter += 1
        if self.interval:
            self.wait()
        else:
            self.channel.close()

    def stop(self):
        self.channel.close()
