data = [('Мат. Анализ', [('Иванов', 15), ('Петров', 13), ('Сидоров', 2), ('Васильев', 10), ('Жуков', 6)]),
        ('Алгебра', [('Петров', 24), ('Иванов', 20), ('Васильев', 11), ('Жуков', 12)]),
        ('Логика', [('Иванов', 10), ('Петров', 15), ('Сидоров', 6)])]


def sum_dictionaries(x):
    def _(y):
        return {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}
    return _


def tuples_to_dict(tuples):
    return {} if len(tuples) == 0 else sum_dictionaries(dict([tuples[0]]))(tuples_to_dict(tuples[1:]))


def get_all_tuples(lst):
    return [] if len(lst) == 0 else lst[0][1] + get_all_tuples(lst[1:])


def get_points_dict(lst):
    return tuples_to_dict(get_all_tuples(lst))


def get_scale(percent):
    def _(value):
        return [] if percent < 40 else [value * percent / 100] + get_scale(percent - 20)(value)
    return _


def get_max_points(lst):
    return max(get_points_dict(lst).values())


def rate_by_scale(scale):
    def _(points):
        return len(scale) + 2 if len(scale) == 0 or scale[0] < points else rate_by_scale(scale[1:])(points)
    return _


def rate_class(lst):
    return list({x[0]: rate_by_scale(get_scale(80)(get_max_points(lst)))(x[1])
                 for x in get_points_dict(lst).items()}.items())


def sorted_rate_class(lst):
    return list(sorted(rate_class(lst), key=lambda x: (-x[1], x[0])))

print(get_scale(80)(get_max_points(data)))
print(sorted_rate_class(data))