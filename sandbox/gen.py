import random

with open("a.txt", "w") as file:
    for i in range(10):
        for j in range(10):
            print("%2d" % random.randint(1, 20), file=file, end=" ")
        print(file=file)

with open("b.txt", "w") as file:
    for i in range(10):
        print("%2d" % random.randint(1, 20), file=file)

with open("e.txt", "w") as file:
    for i in range(10):
        print("%2d" % random.randint(1, 20), file=file)