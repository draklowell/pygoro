from threading import Thread
from typing import Any, Callable, Generic, Iterable, TypeVar

from pygoro.channel import Channel

T = TypeVar("T")


class Goroutine(Thread, Generic[T]):
    function: Callable[..., T] | Iterable[T]
    arguments: list[Any]
    kwarguments: dict[str, Any]
    ret: Channel[T]

    def __init__(
        self,
        function: Callable[..., T] | Iterable[T],
        arguments: list[Any],
        kwarguments: dict[str, Any],
    ) -> None:
        super().__init__()

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


def go(
    function: Callable[..., T] | Iterable[T], *arguments: Any, **kwarguments: Any
) -> Goroutine[T]:
    goroutine = Goroutine(function, arguments, kwarguments)
    goroutine.start()
    return goroutine
