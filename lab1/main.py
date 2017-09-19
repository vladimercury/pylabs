from lab1.classes import Journal, Student
from csv import reader

with open('file.csv', 'r') as file:
    journal = Journal()
    csv_reader = reader(file, delimiter=',', quotechar='"')
    for row in csv_reader:
        name, group, *marks = map(str.strip, row)
        journal.add_student(group, Student(name, marks))
    print(journal)