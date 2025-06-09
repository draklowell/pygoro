import time

from pygoro import go


def test_func(text: str, data: str):
    time.sleep(1)
    print("A")
    print(text, data)


goro = go(test_func, "Hello,", data="World!")
print("B")
for i in goro.ret:
    print(i)
