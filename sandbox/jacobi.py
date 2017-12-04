import numpy as np


def read_matrix(file_name):
    temp = []
    with open(file_name, "r") as file:
        for row in file:
            temp.append(list(map(int, row.split())))
    return np.asarray(temp)


def read_vector(file_name):
    temp = []
    with open(file_name, "r") as file:
        for row in file:
            temp += list(map(int, row.split()))
    return np.asarray(temp)

a = read_matrix("a.txt")
b = read_vector("b.txt")
e = read_vector("e.txt")
l = np.tril(a, -1)
d = a.diagonal()
p = np.triu(a, 1)
