from typing import Any, Callable, Dict, Iterable, List, Union
import threading

from pygoro.channel import Channel, NoObject

GOROUTINE_COUNT = 0
GOROUTINE_NAME = "Goroutine-{id}"


class Goroutine(threading.Thread):
    def __init__(self, function: Union[Callable[..., Any], Iterable[Any]], arguments: List[Any], kwarguments: List[Any]) -> None:
        global GOROUTINE_COUNT
        GOROUTINE_COUNT += 1
        super().__init__(name=GOROUTINE_NAME.format(id=GOROUTINE_COUNT))

        self.function = function
        self.arguments = arguments
        self.kwarguments = kwarguments
        self.ret = Channel()

    def run(self) -> None:
        if isinstance(self.function, Iterable):
            for result in self.function:
                self.ret << result
            self.ret.close()
        else:
            self.ret << self.function(*self.arguments, **self.kwarguments)

def go(function: Union[Callable[..., Any], Iterable[Any]], *arguments: List[Any], **kwarguments: Dict[str, Any]) -> Goroutine:
    goroutine = Goroutine(function, arguments, kwarguments)
    goroutine.start()
    return goroutine
