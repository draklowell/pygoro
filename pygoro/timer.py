import time
from typing import Generator

from pygoro.channel import Channel
from pygoro.goroutine import go


class Timer:
    interval: float
    counter: int
    repeatable: bool
    channel: Channel[float]

    def __init__(self, interval: float, repeatable: bool = False) -> None:
        self.interval = interval
        self.counter = 0
        self.repeatable = repeatable
        self.channel = Channel()
        go(self.wait())

    def wait(self) -> Generator[None, None, None]:
        timeend = time.time() + self.interval
        while not self.channel.closed:
            if time.time() >= timeend:
                break
        else:
            return

        yield from self.finish()

    def finish(self) -> Generator[None, None, None]:
        self.channel << self.counter
        self.counter += 1

        if self.repeatable:
            yield from self.wait()
        else:
            self.channel.close()

    def stop(self) -> None:
        self.channel.close()
