from functools import wraps


def any_instance(*classes_or_types):
    def decorator(function):
        @wraps(function)
        def wrapper(self, value):
            for class_or_type in classes_or_types:
                if isinstance(value, class_or_type):
                    return function(self, value)
            raise AssertionError("Value is not an instance of " + str(classes_or_types))
        return wrapper
    return decorator


def instance(class_or_type):
    def decorator(function):
        @wraps(function)
        def wrapper(self, value):
            if not isinstance(value, class_or_type):
                raise AssertionError("Value is not an instance of " + str(class_or_type))
            return function(self, value)
        return wrapper
    return decorator


def int_number(function):
    return instance(int)(function)


def string(function):
    return instance(str)(function)


def length(minimum, maximum):
    def decorator(function):
        @wraps(function)
        def wrapper(self, value):
            if len(value) < minimum or len(value) > maximum:
                raise AssertionError("Value length does not fit range " + str((minimum, maximum)))
            return function(self, value)
        return wrapper
    return decorator


def in_range(minimum, maximum):
    def decorator(function):
        @wraps(function)
        def wrapper(self, value):
            if value < minimum or value > maximum:
                raise AssertionError("Value does not fit range " + str((minimum, maximum)))
            return function(self, value)
        return wrapper
    return decorator

