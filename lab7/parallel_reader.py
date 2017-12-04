import multiprocessing as mp
from lab7.timer import Timer


def f1(a, b):
    return a - b


def f2(a, b):
    return a + b


def get_lines(file, chunk_size):
    lines = list()
    for _ in range(chunk_size):
        line = file.readline()
        if line:
            lines.append(line)
        else:
            return lines, True
    return lines, False


def do_manager(file_name, chunk_size):
    jobs = list()
    queue = mp.Queue()
    for _ in range(mp.cpu_count()):
        queue.put(0)
    with open(file_name, "r") as file:
        while True:
            queue.get()
            lines, eof = get_lines(file, chunk_size)
            if len(lines) == 0:
                break
            else:
                value = mp.Value("i", 0)
                process = mp.Process(target=worker, args=(lines, queue, value))
                process.start()
                jobs.append((process, value))
                if eof:
                    break
    manager_result = list()
    for job in jobs:
        job[0].join()
        manager_result.append(job[1].value)
    return do_sequence(manager_result)


def worker(lines, shared_queue=None, value=None):
    val = f1(*map(int, lines[0].split()))
    for line in lines[1:]:
        val = f2(val, f1(*map(int, line.split())))
    if shared_queue is None:
        return val
    value.value = val
    shared_queue.put(0)


def do_sequence(data):
    res = f2(data[0], data[1])
    for elem in data[2:]:
        res = f2(res, elem)
    return res


def process_sequence(file_name, chunk_size):
    res = list()
    with open(file_name, "r") as file:
        eof = False
        while not eof:
            lines, eof = get_lines(file, chunk_size)
            if len(lines):
                res.append(worker(lines))
    return do_sequence(res)


if __name__ == "__main__":
    mp.freeze_support()
    timer = Timer()
    print("Processing in parallel...", end="")
    result = do_manager("input.txt", 500000)
    print("done in", timer.diff())
    print("Result =", result)
    timer.reset()
    print("Processing in sequence...", end="")
    result = process_sequence("input.txt", 500000)
    print("done in", timer.diff())
    print("Result =", result)