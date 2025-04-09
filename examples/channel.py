import time

from pygoro import Channel, NoObject, go


def test_func(chan: Channel[int], range_size: int):
    for i in range(range_size):
        time.sleep(1)
        chan <<= i  # same as chan.push(i)
    chan.close()


def test_func_flush(chan: Channel[int], range_size: int):
    for i in range(range_size):
        time.sleep(1)
        chan <<= i  # same as chan.push(i)
        chan <<= NoObject  # same as chan.flush()
    chan.close()


def read_chan(chan: Channel[int]):
    for i in chan:
        print(i)


chan_unbuffered = Channel[int]()
go(test_func, chan_unbuffered, 5)
print("testFunc(chanUnbuffered)")
read_chan(chan_unbuffered)

chan_buffered = Channel[int](2)
go(test_func, chan_buffered, 5)
print("testFunc(chanBuffered)")
read_chan(chan_buffered)

chan_buffered = Channel[int](2)
go(test_func_flush, chan_buffered, 5)
print("testFuncFlush(chanBuffered)")
read_chan(chan_buffered)
