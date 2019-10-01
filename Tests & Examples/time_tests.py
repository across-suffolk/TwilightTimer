import datetime

# time(hour = 0, minute = 0, second = 0)
a = datetime.time()
print("a =", a)

# time(hour, minute and second)
b = datetime.time(11, 34)
print("b =", b)

# time(hour, minute and second)
c = datetime.time(hour = 11, minute = 34, second = 56)
print("c =", c)

# time(hour, minute, second, microsecond)
d = datetime.time(11, 34, 56, 234566)
print("d =", d)