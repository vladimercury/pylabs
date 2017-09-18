class Student:
    def __init__(self, name, marks, max_marks_count=5, default_mark=2):
        self.name = name
        self.marks = marks[:max_marks_count] + [default_mark] * (max_marks_count - len(marks))
        self.marks = list(map(int, self.marks))
        self.average = sum(self.marks) / len(marks) if len(marks) > 0 else 0

    def __str__(self):
        row = (self.name, str(self.average), ' '.join(map(str, self.marks)))
        return ' '.join(row)