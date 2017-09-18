class Group:
    def __init__(self, name):
        self.name = name
        self.students = list()

    def __str__(self):
        students_list = "\n".join(map(str, self.students))
        return students_list


from lab1.Student import Student
