class Student:
    def __init__(self, name, marks, max_marks_count=5, default_mark=2):
        self.name = name
        self.marks = marks[:max_marks_count] + [default_mark] * (max_marks_count - len(marks))
        self.marks = list(map(int, self.marks))
        self.average = sum(self.marks) / len(self.marks) if len(self.marks) > 0 else 0

    def __str__(self):
        row = (self.name, str(self.average), ' '.join(map(str, self.marks)))
        return ' '.join(row)


class Group:
    def __init__(self, name):
        self.name = name
        self.students = list()

    def __str__(self):
        self.students.sort(key=lambda s: (-s.average, s.name))
        rows = ['Группа ' + self.name + ':']
        rows += map(str, self.students)
        return "\n".join(rows)

    def add(self, student):
        self.students.append(student)


class Journal:
    def __init__(self):
        self.groups = dict()

    def add(self, group_name, student):
        if group_name not in self.groups:
            self.groups[group_name] = Group(group_name)
        self.groups[group_name].add(student)

    def __str__(self):
        parts = list()
        for group_name in sorted(self.groups.keys()):
            group = self.groups[group_name]
            parts.append(str(group))
        return "\n\n".join(parts)