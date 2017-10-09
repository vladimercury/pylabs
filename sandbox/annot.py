import functools
import inspect


def type_check(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        arg_spec = inspect.getfullargspec(function)
        arg_list = arg_spec.args
        annotations = arg_spec.annotations
        for index in range(len(arg_list)):
            arg_name = arg_list[index]
            if arg_name in annotations:
                arg_type = annotations[arg_name]
                if type(args[index]) != arg_type:
                    raise AssertionError("%s must be instance of %s" % (arg_name, arg_type))
        return function(*args, **kwargs)
    return wrapper


@type_check
def my_func(name: str, age: int, is_student: bool) -> tuple:
    return name, age, is_student


print(my_func("a", 2, True))