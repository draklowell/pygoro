from collections import deque
from threading import Lock
from typing import Generic, Iterator, TypeVar


class NoObjectType:
    pass


NoObject = NoObjectType()

T = TypeVar("T")


class Channel(Generic[T]):
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
        self.lock = Lock()

    def __lshift__(self, value: T | NoObjectType) -> None:
        self.push(value)

    def __next__(self) -> T:
        while (not self.closed) and not self.queue:
            continue

        if self.closed and not self.queue:
            return StopIteration

        return self.queue.popleft()

    def __iter__(self) -> Iterator[T]:
        while not self.closed or self.queue:
            if not self.queue:
                continue

            yield self.queue.popleft()

    def flush(self) -> None:
        with self.lock:
            self.queue.extend(self.buffer)
            self.buffer.clear()

    def push(self, value: T | NoObjectType) -> None:
        if isinstance(value, NoObjectType):
            self.flush()
            return

        self.buffer.append(value)

        if len(self.buffer) >= self.buffer_size:
            self.flush()

    def get(self, default: T | NoObjectType = NoObject) -> T | NoObjectType:
        if not self.queue:
            return default

        return self.queue.popleft()

    def close(self) -> None:
        self.closed = True
