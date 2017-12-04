data = [('Мат. Анализ', [('Иванов', 15), ('Петров', 13), ('Сидоров', 2), ('Васильев', 10), ('Жуков', 6)]),
        ('Алгебра', [('Петров', 24), ('Иванов', 20), ('Васильев', 11), ('Жуков', 12)]),
        ('Логика', [('Иванов', 10), ('Петров', 15), ('Сидоров', 6), ('Жуков', 15)])]


def points_per_student(lst):
    def _(course):
        pass


def all_points(lst):
    return [] if len(lst) == 0 else lst[0][1] + all_points(lst[1:])


def points_single(surname):
    def _(lst):
        return sum(map(lambda x: x[1], filter(lambda x: x[0] == surname, all_points(lst))))
    return _


def max_score(lst):
    return max(map(lambda x: points_single(x[0])(lst), all_points(lst)))


def scale(stage):
    def _(val):
        return [] if stage < 40 else [val * stage / 100.0] + scale(stage - 20)(val)
    return _


def points_all(lst):
    return list(map(lambda x: (x[0], points_single(x[0])(lst)), all_points(lst)))

print(all_points(data))
print(scale(80)(max_score(data)))
