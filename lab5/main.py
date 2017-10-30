import lab5.restrictions as restrictions


class Person:
    def __init__(self, name, passport_number):
        self.name = name
        self.passport_number = passport_number

    def _get_name(self):
        return self.__name

    @restrictions.string
    @restrictions.length(1, 20)
    def _set_name(self, value):
        self.__name = value

    def _get_passport(self):
        return self.__passport

    def _set_passport(self, value):
        self.__passport = value

    name = property(_get_name, _set_name)
    passport_number = property(_get_passport, _set_passport)


x = Person("MyName")