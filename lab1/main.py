# Read from CSV file
def read_from_file(file_name):
    import csv
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')
        return list(csv_reader)


data = read_from_file('file.csv')
journal = dict()

# Filling journal
for row in data:
    row = map(str.strip, row)
    name, group_name, *marks = row
    marks += ['2'] * (5 - len(marks))
    marks = list(map(int, marks))
    student = (name, sum(marks) / 5, marks)
    if group_name not in journal:
        journal[group_name] = list()
    journal[group_name].append(student)

# Sorting journal
for group in journal.values():
    group.sort(key=lambda z: (-z[1], z[0]))

for group_name in sorted(journal.keys()):
    print('Группа', group_name + ':')
    for student in journal[group_name]:
        name, mark, marks = student
        print(name, mark, ' '.join(map(str, marks)))