import time

from pygoro import go


def test_func(text: str, data: str) -> int:
    time.sleep(1)
    print("A")
    print(text, data)
    return 10


goro = go(test_func, "Hello,", data="World!")
print("B")
for i in goro.ret:
    print(i)
