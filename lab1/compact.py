import csv

DEFAULT_MARK = 2
MARKS_LEN = 5

with open('file.csv', 'r') as file:
    journal = dict()
    csv_reader = csv.reader(file, delimiter=',', quotechar='"')
    for row in csv_reader:
        name, group_name, *marks = map(str.strip, row)
        marks = list(map(int, marks))
        marks += [DEFAULT_MARK] * (MARKS_LEN - len(marks))
        student = (name, sum(marks) / MARKS_LEN, marks)
        if group_name not in journal:
            journal[group_name] = list()
        journal[group_name].append(student)

    for group_name, group in sorted(journal.items()):
        group.sort(key=lambda z: (-z[1], z[0]))
        print('Группа', group_name + ':')
        for student in group:
            name, mark, marks = student
            print(name, mark, ' '.join(map(str, marks)))
        print()