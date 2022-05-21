from pygoro import go
import time

def test_func(text, data):
    time.sleep(1)
    print("A")
    print(text, data)

go(test_func, "Hello,", data="World!")
print("B")
