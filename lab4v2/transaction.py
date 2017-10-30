import datetime


class Transaction:
    def __init__(self, bank, src_id: str, dst_id: str, cash: float, currency: str, course: float):
        self.__bank = bank
        self.__src = src_id
        self.__dst = dst_id
        self.__cash = cash
        self.__currency = currency
        self.__base_currency = bank.base_currency
        self.__course = course
        self.__time = datetime.datetime.now()

    @property
    def source_id(self) -> str:
        return self.__src

    @property
    def source(self):
        return self.__bank.get_account(self.__src)

    @property
    def destination_id(self) -> str:
        return self.__dst

    @property
    def destination(self):
        return self.__bank.get_account(self.__dst)

    @property
    def cash(self) -> float:
        return self.__cash

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def base_currency(self) -> str:
        return self.__base_currency

    @property
    def course(self) -> float:
        return self.__course

    @property
    def time(self) -> datetime.datetime:
        return self.__time

    def is_foreign(self) -> bool:
        return self.__base_currency != self.__currency

    def __str__(self):
        formatter = "%s -> %s: %.2f %s at %s"
        args = (self.__src, self.__dst, self.__cash, self.__currency, self.__time)
        if self.is_foreign():
            formatter += " (%.2f %s with course %.8f %s/%s)"
            args = args + (self.__cash * self.__course, self.__base_currency, self.__course, self.__currency,
                           self.__base_currency)
        return formatter % args
