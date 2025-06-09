from collections import deque
from threading import Lock, RLock
from typing import Generic, Iterator, TypeVar


class NoObjectType:
    """A class to represent a no object type."""


NoObject = NoObjectType()

T = TypeVar("T")


class Channel(Generic[T]):
    """
    Channel class to implement a thread-safe channel for communication
    between goroutines. It allows pushing and pulling values in a
    blocking manner, with an optional buffer size to control the number
    of items that can be buffered before being pushed to the queue.

    Args:
        buffer_size: The size of the buffer. Defaults to 1.

    Attributes:
        queue: A deque to hold the values in the channel.
        buffer: A deque to hold the buffered values before pushing to the queue.
        buffer_size: The size of the buffer.
        closed: A boolean indicating if the channel is closed.
        read_lock: A lock to ensure thread-safe reading from the channel.
        write_lock: A reentrant lock to ensure thread-safe writing to the channel.
    """

    queue: deque
    buffer: deque
    buffer_size: int
    closed: bool
    read_lock: Lock
    write_lock: Lock

    def __init__(self, buffer_size: int = 1) -> None:
        self.queue = deque()
        self.buffer = deque()
        self.buffer_size = buffer_size
        self.closed = False
        self.read_lock = Lock()
        self.write_lock = RLock()

    def __lshift__(self, value: T | NoObjectType) -> None:
        self.push(value)

    def __ilshift__(self, value: T | NoObjectType) -> None:
        self.push(value)
        return self

    def __next__(self) -> T:
        with self.read_lock:
            while (not self.closed) and not self.queue:
                continue

            if self.closed and not self.queue:
                return StopIteration

            return self.queue.popleft()

    def __iter__(self) -> Iterator[T]:
        while not self.closed or self.queue:
            with self.read_lock:
                if not self.queue:
                    continue

                yield self.queue.popleft()

    def flush(self) -> None:
        """
        Flush the buffer to the queue.

        **It is a blocking operation.**
        """
        with self.write_lock:
            self.queue.extend(self.buffer)
            self.buffer.clear()

    def push(self, value: T | NoObjectType) -> None:
        """
        Push a value to the channel.

        **It is a blocking operation.**

        Args:
            value: The value to push to the channel.
        """
        with self.write_lock:
            if isinstance(value, NoObjectType):
                self.flush()
                return

            self.buffer.append(value)

            if len(self.buffer) >= self.buffer_size:
                self.flush()

    def get(self, default: T | NoObjectType = NoObject) -> T | NoObjectType:
        """
        Get a value from the channel.

        **It is a blocking operation.**

        Args:
            default: The default value to return if the queue is empty.
                     Defaults to NoObject.

        Returns:
            The value from the queue or the default value.
        """
        with self.read_lock:
            if not self.queue:
                return default

            return self.queue.popleft()

    def close(self) -> None:
        """
        Close the channel.
        """
        self.closed = True
