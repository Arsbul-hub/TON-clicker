step = int(input())
m = input()

for i in m:
    if ord(i) <= ord("я") and ord(i) >= ord("а"):
        o = ord(i) + step
        if o > ord("я"):
            o -= 32
        print(chr(o), end="")
    elif ord(i) <= ord("Я") and ord(i) >= ord("А"):
            o = ord(i) + step
            if o > ord("Я"):
                o -= 32
            print(chr(o), end="")
    else:
        print(i, end="")