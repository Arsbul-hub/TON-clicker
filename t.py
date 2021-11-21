st = int(input())
cur_user = "ai"
step = 0
while st > 0:
    if cur_user == "ai":
        if st < 4:
            step = st
        else:
            step = st % 4
        if step == 0:
            step = 1
        st -= step
        print(step, st)
        cur_user = "user"

    else:
        step = int(input())
        while step < 1 or step > 3 or step > st:
            print(f"Некорректный ход: {step}")
            step = int(input())

        st -= step
        print(step, st)
        cur_user = "ai"

if cur_user == "ai":
    print("Вы выиграли!")
else:
    print("ИИ выиграл!")
