import collections


def size(sized: collections.Sized, expected_size: int) -> None:
    if len(sized) != expected_size:
        raise AssertionError("Size doesn't fit expected size")


def all_positive(iterable: collections.Iterable) -> None:
    for element in iterable:
        if element <= 0:
            break
    else:
        return
    raise AssertionError("Not all elements are positive")