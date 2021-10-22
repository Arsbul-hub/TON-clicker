a = float(input())
b = float(input())
s = input()
if s == "/" and b == 0 or (s != "+" and s != "-" and s != "*" and s != "/"):
    print(888888)
if s == "+":
    print(a + b)
if s == "-":
    print(a - b)
if s == "*":
    print(a * b)
if s == "/":
    print(a / b)
