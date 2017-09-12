# Read csv files
import csv

with 'file.csv' as file:
    csv_reader = csv.reader(file, delimeter=',', quotechar='"')
    for row in csv_reader:
        print(row[0])