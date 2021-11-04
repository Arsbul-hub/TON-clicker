import random
import pickle
import datetime
from statistics import mean
time = []
for i in range(5):
    a = []
    b = []
    old_time = datetime.datetime.now().time().second
    for i in range(1000000):
        a.append(random.randint(0,1000))
        b.append(random.randint(0,1000))
    a.sort()
    b.sort()
    c = set(a)
    d = set(b)
    new_time = datetime.datetime.now().time().second * datetime.datetime.now().time().minute
    time.append(new_time - old_time)
    if c == d:

        print(c,d)


print(f"{mean(time)} seconds" )
