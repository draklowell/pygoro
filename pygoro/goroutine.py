from typing import Any, Callable, Dict, List
import threading


GOROUTINE_COUNT = 0
GOROUTINE_NAME = "Goroutine-{id}"

class Goroutine(threading.Thread):
    def __init__(self, function: Callable[..., Any], arguments: List[Any], kwarguments: List[Any]) -> None:
        global GOROUTINE_COUNT
        GOROUTINE_COUNT += 1
        super().__init__(target=function, args=arguments, kwargs=kwarguments, name=GOROUTINE_NAME.format(id=GOROUTINE_COUNT))
        self.start()

def go(function: Callable[..., Any], *arguments: List[Any], **kwarguments: Dict[str, Any]) -> Goroutine:
    return Goroutine(function, arguments, kwarguments)
