from typing import Any, Optional
import threading
from collections import deque


class NoObject:
    pass

class Channel:
    queue: deque
    buffer: deque
    buffer_size: int
    closed: bool
    read_lock: threading.Lock
    write_lock: threading.Lock

    def __init__(self, buffer_size: Optional[int] = 1) -> None:
        self.queue = deque()
        self.buffer = deque()
        self.buffer_size = buffer_size
        self.closed = False
        self.lock = threading.Lock()

    def __lshift__(self, value) -> None:
        self.push(value)

    def __next__(self) -> Any:
        while (not self.closed) and not self.queue:
            continue

        if self.closed and not self.queue:
            return StopIteration

        return self.queue.popleft()

    def __iter__(self) -> Any:
        while not self.closed or self.queue:
            if not self.queue:
                continue

            yield self.queue.popleft()

    def flush(self) -> None:
        with self.lock:
            self.queue.extend(self.buffer)
            self.buffer.clear()

    def push(self, value: Any) -> None:
        if value == NoObject:
            self.flush()
            return

        self.buffer.append(value)

        if len(self.buffer) >= self.buffer_size:
            self.flush()

    def get(self, default: Any = NoObject) -> Any:
        if not self.queue:
            return default

        return self.queue.popleft()

    def close(self) -> None:
        self.closed = True
