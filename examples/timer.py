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
