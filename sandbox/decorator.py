from functools import wraps


def positive_result(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result > 0
        return result
    return wrapper


def minimum_result(minimum):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result < minimum:
                raise AssertionError()
            return result
        return wrapper
    return decorator


@minimum_result(4)
def my_func(n):
    return n


my_func(5)
my_func(4)
my_func(3)