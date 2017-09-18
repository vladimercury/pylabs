from lab1.classes import Journal, Student
from csv import reader

with open('file.csv', 'r') as file:
    journal = Journal()
    csv_reader = reader(file, delimiter=',', quotechar='"')
    for row in csv_reader:
        name, group, *marks = row
        journal.add(group.strip(), Student(name, marks))
    print(journal)