from functools import wraps


def length(start, end):
    def decorator(function):
        @wraps(function)
        def wrapper(self, value):
            if len(value) < start or len(value) > end:
                raise AssertionError("Value length does not fits range")
            return function(self, value)
        return wrapper
    return decorator


def string(function):
    @wraps(function)
    def wrapper(self, value):
        if not isinstance(value, str):
            raise AssertionError("Value is not a string")
        return function(self, value)
    return wrapper
