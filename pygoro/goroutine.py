from threading import Thread
from typing import Any, Callable, Generic, Iterator, TypeVar

from pygoro.channel import Channel

T = TypeVar("T")


class Goroutine(Thread, Generic[T]):
    """
    Goroutine class that extends Thread to run a function or generator
    in a separate thread. It can be used to run a function or generator
    in the background and communicate with it using channels.

    Args:
        function: Function or generator to run in goroutine.
        arguments: Positional arguments for the function.
        kwarguments: Keyword arguments for the function.

    Attributes:
        function: The function or generator to run.
        arguments: Positional arguments for the function.
        kwarguments: Keyword arguments for the function.
        ret: Channel to communicate with the goroutine.
    """

    function: Callable[..., T] | Iterator[T]
    arguments: list[Any]
    kwarguments: dict[str, Any]
    ret: Channel[T]

    def __init__(
        self,
        function: Callable[..., T] | Iterator[T],
        arguments: list[Any],
        kwarguments: dict[str, Any],
    ) -> None:
        super().__init__()

        self.function = function
        self.arguments = arguments
        self.kwarguments = kwarguments
        self.ret = Channel()

    def run(self) -> None:
        """
        Run the goroutine. If the function is a generator, it will yield
        values to the channel until it is closed. If the function is a
        callable, it will call the function with the provided arguments
        and keyword arguments and send the result to the channel.
        """
        if isinstance(self.function, Iterator):
            for result in self.function:
                self.ret <<= result
        else:
            self.ret <<= self.function(*self.arguments, **self.kwarguments)

        self.ret.close()


def go(
    function: Callable[..., T] | Iterator[T],
    *arguments: Any,
    **kwarguments: Any,
) -> Goroutine[T]:
    """
    Create a goroutine from function or generator and start it.

    If the function is a generator, it will yield values to the
    channel until it is closed. If the function is a callable,
    it will call the function with the provided arguments and
    keyword arguments and send the result to the channel.

    Args:
        function: Function or generator to run in goroutine.
        *arguments: Positional arguments for the function.
        **kwarguments: Keyword arguments for the function.

    Returns:
        The created goroutine. You can access the return value using `goroutine.ret`.
    """
    goroutine = Goroutine(function, arguments, kwarguments)
    goroutine.start()
    return goroutine
