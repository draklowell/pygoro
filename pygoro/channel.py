from typing import Any, List, Optional
import threading


class NoObject:
    pass

class Channel:
    queue: List
    buffer: List
    buffer_size: int
    closed: bool
    lock: threading.Lock

    def __init__(self, buffer_size: Optional[int] = 1) -> None:
        self.queue = []
        self.buffer = []
        self.buffer_size = buffer_size
        self.closed = False
        self.lock = threading.Lock()

    def __lshift__(self, value) -> None:
        self.push(value)
    
    def __next__(self) -> Any:
        while (not self.closed) and len(self.queue) < 1:
            continue
        if self.closed and len(self.queue) < 1:
            return StopIteration
        return self.queue.pop(0)

    def __iter__(self) -> Any:
        while True:
            while (not self.closed) and len(self.queue) < 1:
                continue
            if self.closed and len(self.queue) < 1:
                break
            yield self.queue.pop(0)

    def flush(self) -> None:
        with self.lock:
            self.queue += self.buffer
            self.buffer = []

    def push(self, value: Any) -> None:
        if value == NoObject:
            self.flush()
            return
        self.buffer.append(value)
        if len(self.buffer) >= self.buffer_size:
            self.flush()

    def get(self, default: Any = NoObject) -> Any:
        if len(self.queue) < 1:
            return default
        return self.queue.pop(0)

    def close(self) -> None:
        self.closed = True
