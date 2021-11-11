import random
import pickle
import datetime
from statistics import mean
time = []
for i in range(5):
    a = []
    b = []
    c = []
    d = []

    for i in range(1000000):
        a.append(random.randint(0,1000))
        b.append(random.randint(0, 1000))
    old_time = datetime.datetime.now().time().second
    for i in a:
        if i not in d:
            d.append(i)
    for i in b:
        if i not in c:
            c.append(i)
    d.sort()
    c.sort()
    #c = set(a)
    #d = set(b)
    new_time = datetime.datetime.now().time().second
    time.append(new_time - old_time)
    #print(a,b)
    if c == d:
        print("True")
    else:
        print("False")


print(f"{mean(time)} seconds" )
