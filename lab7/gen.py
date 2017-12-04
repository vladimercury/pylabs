from random import randint

with open("input.txt", "w") as file:
    for i in range(1000):
        for j in range(5000):
            print(randint(-100, 100), randint(-100, 100), file=file)
        print("\r%.1f%%" % ((i + 1) / 10), end="")