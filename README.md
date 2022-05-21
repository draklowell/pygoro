# PyGoro
Go goroutines and channels implementation in python
### Usage examples
Goroutines
```python
from pygoro import go
import time

def test_func(text, data):
    time.sleep(1)
    print("A")
    print(text, data)

go(test_func, "Hello,", data="World!")
print("B")

# B
# A
# Hello, World!
```
Channels
```python
from pygoro import go, Channel, NoObject
import time

def test_func(chan, range_size):
    for i in range(range_size):
        time.sleep(1)
        chan << i # same as chan.push(i)
    chan.close()

def test_func_flush(chan, range_size):
    for i in range(range_size):
        time.sleep(1)
        chan << i # same as chan.push(i)
        chan << NoObject # same as chan.flush()
    chan.close()

def read_chan(chan):
    for i in chan:
        print(i)

chan_unbuffered = Channel()
go(test_func, chan_unbuffered, 5)
print("testFunc(chanUnbuffered)")
read_chan(chan_unbuffered)

chan_buffered = Channel(2)
go(test_func, chan_buffered, 5)
print("testFunc(chanBuffered)")
read_chan(chan_buffered)

chan_buffered = Channel(2)
go(test_func_flush, chan_buffered, 5)
print("testFuncFlush(chanBuffered)")
read_chan(chan_buffered)

# testFunc(chanUnbuffered)
# 0
# 1
# 2
# 3
# 4
# testFunc(chanBuffered)
# 0
# 1
# 2
# 3
# testFuncFlush(chanBuffered)
# 0
# 1
# 2
# 3
# 4
```
Timer
```python
from pygoro import Timer

print("timer 1 interval")
timer = Timer(1, True)
for i in timer.channel:
    print(i)
    if i >= 4:
        timer.stop()

print("timer 1")
timer = Timer(1)
for i in timer.channel:
    print(i)
    if i >= 4:
        timer.stop()

# timer 1 interval
# 0
# 1
# 2
# 3
# 4
# timer 1
# 0
```
