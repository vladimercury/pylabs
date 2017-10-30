import lab5.restrictions as restrictions
from datetime import date, datetime
from csv import reader
from sys import stderr


class Person:
    __date_format = "%d.%m.%Y"

    @classmethod
    def from_row(cls, row):
        name, surname, passport, birth_date = row
        passport = int(passport)
        birth_date = datetime.strptime(birth_date, cls.__date_format).date()
        return Person(name, surname, passport, birth_date)

    def __init__(self, name, surname, passport_number, birth_date):
        self.name = name
        self.surname = surname
        self.passport_number = passport_number
        self.birth_date = birth_date

    def _get_surname(self):
        return self.__surname

    @restrictions.string
    @restrictions.length(1, 20)
    def _set_surname(self, value):
        self.__surname = value

    def _get_name(self):
        return self.__name

    @restrictions.string
    @restrictions.length(1, 20)
    def _set_name(self, value):
        self.__name = value

    def _get_passport(self):
        return self.__passport

    @restrictions.int_number
    @restrictions.in_range(100000, 999999)
    def _set_passport(self, value):
        self.__passport = value

    def _get_birth_date(self):
        return self.__birth_date

    @restrictions.instance(date)
    @restrictions.in_range(date(1900, 1, 1), datetime.now().date())
    def _set_birth_date(self, value):
        self.__birth_date = value

    def __str__(self):
        parts = [self.name, self.passport_number, self.birth_date.strftime(self.__date_format)]
        return "%s{{ %s }}" % (str(self.__class__), ", ".join(map(str, parts)))

    name = property(_get_name, _set_name)
    surname = property(_get_surname, _set_surname)
    passport_number = property(_get_passport, _set_passport)
    birth_date = property(_get_birth_date, _set_birth_date)


class PersonCSVLoader:
    class ParsingException(Exception):
        def __init__(self, error_or_message, line):
            self.__child = None
            if isinstance(error_or_message, Exception):
                self.__child = type(error_or_message).__name__
            super(PersonCSVLoader.ParsingException, self).__init__(str(error_or_message))
            self.__line = line

        def __str__(self):
            if self.__child:
                return "%s at line %d: %s" % (self.__child, self.__line, self.args[0])
            else:
                return "Exception at line %d: %s" % (self.__line, self.args[0])

    @staticmethod
    def load(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            csv_reader = reader(file, delimiter=',', quotechar='"')
            row_number = 0
            for row in csv_reader:
                row_number += 1
                try:
                    yield Person.from_row(row)
                except (AssertionError, ValueError) as err:
                    print(PersonCSVLoader.ParsingException(err, row_number), file=stderr)


try:
    for person in PersonCSVLoader.load("persons.csv"):
        print(person)
except PersonCSVLoader.ParsingException as ex:
    print(ex, file=stderr)
