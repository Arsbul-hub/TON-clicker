x = int(input())
y = int(input())
px = 0
py = 0
n = 0
v = 0
while True:
    rot = input()
    if rot == "стоп":
        break
    steps = int(input())
    if rot == "север":
        py += steps
    if rot == "юг":
        py -= steps
    if rot == "запад":
        px -= steps
    if rot == "восток":
        px += steps
    n += 1
    if x == px and y == py and v == 0:
        v = n

print(v)