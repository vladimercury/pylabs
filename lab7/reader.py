import multiprocessing as mp
from lab7.timer import Timer


def do_sequence():
    with open("input.txt", "r") as file:
        for row in file:
            x = map(int, row.split())


def do_job(file):
    with lock:
        for _ in range(1000):
            line = file.readline()
            if line == "":
                break
            x = map(int, line.split())


def init_child(lock_):
    global lock
    lock = lock_


def do_parallel():
    lock = mp.Lock()
    with open("input.txt") as file:
        with mp.Pool(mp.cpu_count(), initializer=init_child, initargs=(lock,)) as pool:
            pool.imap_unordered(do_job, [file] * mp.cpu_count())



if __name__ == "__main__":
    mp.freeze_support()
    timer = Timer()
    timer.reset()
    # do_sequence()
    print(timer.diff())
    timer.reset()
    do_parallel()
    print(timer.diff())


print(type(open("input.txt", "r").readlines()))