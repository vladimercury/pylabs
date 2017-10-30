import lab5.restrictions as restrictions
from datetime import date, datetime
from csv import reader, writer
from sys import stderr
from lxml import etree


class MakeCSV:
    def __init__(self, *args):
        self.__attr = args

    def __get__(self, instance, owner):
        parts = list()
        for attr, attr_type in self.__attr:
            attr_value = instance.__dict__[attr]
            if attr_type == datetime.date:
                parts.append(attr_value.strftime(instance.get_date_format()))
            else:
                parts.append(str(attr_value))
        return parts


class MakeXML:
    def __init__(self, *args):
        self.__attr = args

    def __get__(self, instance, owner):
        root = etree.Element(owner.__name__)
        replaced = "_" + owner.__name__ + "__"
        for attr, attr_type in self.__attr:
            attr_value = instance.__dict__[attr]
            child = etree.Element(attr.replace(replaced, ""))
            if attr_type == datetime.date:
                child.text = attr_value.strftime(instance.get_date_format())
            else:
                child.text = str(attr_value)
            root.append(child)
        return root


class Person:
    __attributes = (
        ("_Person__name", str),
        ("_Person__surname", str),
        ("_Person__passport", int),
        ("_Person__birth_date", datetime.date)
    )
    __date_format = "%d.%m.%Y"
    csv_data = MakeCSV(*__attributes)
    xml_data = MakeXML(*__attributes)

    @classmethod
    def from_row(cls, row):
        name, surname, passport, birth_date = row
        passport = int(passport)
        birth_date = datetime.strptime(birth_date, cls.__date_format).date()
        return Person(name, surname, passport, birth_date)

    @classmethod
    def get_date_format(cls):
        return cls.__date_format

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
    @restrictions.in_range(date(1800, 1, 1), datetime.now().date())
    def _set_birth_date(self, value):
        self.__birth_date = value

    def __str__(self):
        return "%s{{ %s }}" % (str(self.__class__), ", ".join(self.csv_data))

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
                    raise PersonCSVLoader.ParsingException(err, row_number)


def read_from_csv(filename):
    try:
        return [person for person in PersonCSVLoader.load(filename)]
    except PersonCSVLoader.ParsingException as ex:
        print(ex, file=stderr)
        return None


def write_to_csv(filename, persons):
    with open(filename, "w", newline='') as file:
        csv_writer = writer(file)
        for person in persons:
            csv_writer.writerow(person.csv_data)


def write_to_xml(filename, persons):
    with open(filename, "w") as file:
        root = etree.Element("root")
        for person in persons:
            root.append(person.xml_data)
        file.write(etree.tostring(root, pretty_print=True).decode("utf-8"))


read_from_csv("persons.csv")
person_list = read_from_csv("persons_norm.csv")
if person_list is not None:
    write_to_csv("reflection.csv", person_list)
    write_to_xml("reflection.xml", person_list)
