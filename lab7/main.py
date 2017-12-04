from lab7.timer import Timer
import multiprocessing as mp
import numpy as np
from random import randint
import math

if __name__ == "__main__":
    mp.freeze_support()


def f1(a, b):
    return a - b


def f2(a, b):
    return a + b


def read_data():
    with open("input.txt", "r") as file:
        tmp = []
        for row in file:
            first, second = map(int, row.split())
            tmp.append(f1(first, second))
    return tmp


def generate_data(n):
    return [randint(-100, 100) for i in range(n)]


def simulate_read_data(n=1000000, parallel=True):
    if parallel:
        n_cpu = mp.cpu_count()
        data = mp.Pool(processes=n_cpu).map(generate_data, [n // n_cpu] * n_cpu, chunksize=1)
        res = []
        for part in data:
            res += part
        return res
    else:
        return generate_data(n)


def do_sequence(data):
    res = f2(data[0], data[1])
    for elem in data[2:]:
        res = f2(res, elem)
    return res


def array_slice(array, n_parts):
    lsp = np.linspace(0, len(array), n_parts + 1)
    lsp = list(map(math.ceil, lsp))
    return [array[lsp[i]:lsp[i+1]] for i in range(len(lsp)-1)]


def do_parallel(data):
    n_cpu = mp.cpu_count()
    slices = array_slice(data, n_cpu * 1000)
    return do_sequence(mp.Pool(processes=n_cpu).map(do_sequence, slices))

if __name__ == "__main__":
    timer = Timer()
    print("Reading data...", end="")
    collected = read_data()
    print("done in", timer.diff())
    timer.reset()
    print("Processing...", end="")
    result = do_sequence(collected)
    print("done in", timer.diff())
    print("Result =", result)
    timer.reset()