class Student:
    def __init__(self, name, marks):
        if not isinstance(name, str):
            raise TypeError("name must be string")
        if not isinstance(marks, list):
            raise TypeError("marks must be list")
        self.name = name
        self.marks = list(map(int, marks))


class Group:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be string")
        self.name = name
        self.students = list()

    def add(self, student):
        if not isinstance(student, Student):
            raise TypeError("student is not instance of Student")
        self.students.append(student)


class Journal:
    def __init__(self, min_mark_list_length=5, default_mark=2):
        if not isinstance(min_mark_list_length, int):
            raise TypeError("Min mark list length must be int")
        if min_mark_list_length < 1:
            raise ValueError("Min mark list length must be more than zero")
        if not isinstance(default_mark, int):
            raise TypeError("Default mark must be int")
        self.groups = dict()
        self.min_mark_list_length = min_mark_list_length
        self.default_mark = default_mark

    def get_group(self, group_name):
        if not isinstance(group_name, str):
            raise TypeError("Group name must be string")
        if group_name not in self.groups:
            self.groups[group_name] = Group(group_name)
        return self.groups[group_name]

    def add_student(self, group_name, student):
        if not isinstance(group_name, str):
            raise TypeError("Group name must be string")
        if not isinstance(student, Student):
            raise TypeError("Student is not instance of Student")
        group = self.get_group(group_name)
        group.add(student)

    def _get_extended_mark_list(self, marks):
        extension = [self.default_mark] * (self.min_mark_list_length - len(marks))
        return marks + extension

    def _get_group_performance(self, group):
        if not isinstance(group, Group):
            raise TypeError("Group is not instance of Group")
        performance_list = list()
        for student in group.students:
            extended_mark_list = self._get_extended_mark_list(student.marks)
            average_score = sum(extended_mark_list) / len(extended_mark_list)
            student_performance = (student.name, average_score) + tuple(extended_mark_list)
            performance_list.append(student_performance)
        performance_list.sort(key=lambda perf: (-perf[1], perf[0]))
        lines = [" ".join(map(str, entry)) for entry in performance_list]
        return "\n".join(lines)

    def _get_group_journal(self, group):
        if not isinstance(group, Group):
            raise TypeError("Group is not instance of Group")
        return "\n".join(["Группа %s:" % group.name, self._get_group_performance(group)])

    def __str__(self):
        parts = list()
        for group_name, group in sorted(self.groups.items()):
            parts.append(self._get_group_journal(group))
        return "\n\n".join(parts)