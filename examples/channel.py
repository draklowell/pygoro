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
