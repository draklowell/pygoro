import time
from typing import Generator

from pygoro.channel import Channel
from pygoro.goroutine import go


class Timer:
    """
    Timer class to create a timer that sends a value to a channel
    after a specified interval. The timer can be repeatable or one-time.

    Args:
        interval: The time interval in seconds.
        repeatable: If True, the timer will repeat after the interval.
                    If False, the timer will stop after one interval.

    Attributes:
        interval: The time interval in seconds.
        counter: The number of times the timer has triggered.
        repeatable: If True, the timer will repeat after the interval.
        channel: The channel to send the timer value to.
    """

    interval: float
    counter: int
    repeatable: bool
    channel: Channel[float]

    def __init__(self, interval: float, repeatable: bool = False) -> None:
        self.interval = interval
        self.counter = 0
        self.repeatable = repeatable
        self.channel = Channel()
        go(self.run())

    def run(self) -> Generator[None, None, None]:
        """
        Run the timer.
        """
        end = time.time() + self.interval
        while not self.channel.closed:
            if time.time() >= end:
                self.channel <<= self.counter
                self.counter += 1

                if not self.repeatable:
                    break

                end += self.interval
        else:
            return

        self.channel.close()
        yield

    def stop(self) -> None:
        """
        Stop the timer and close the channel.
        """
        self.channel.close()
