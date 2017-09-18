class Student:
    def __init__(self, name, marks, max_marks_count=5, default_mark=2):
        self.name = name
        self.marks = marks[:max_marks_count] + [default_mark] * (max_marks_count - len(marks))
        self.marks = list(map(int, self.marks))
        self.average = sum(self.marks) / len(marks) if len(marks) > 0 else 0

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

    def add_student(self, student):
        self.students.append(student)

x = Student('Иванов', [3,3,3])
y = Student('Иванов', [5,5,3])

g = Group('M4105')
g.add_student(x)
g.add_student(y)
print(g)