import datetime


class Transaction:
    def __init__(self, source, destination, amount: float, currency: str, course: float = 1):
        self.__source = source
        self.__destination = destination
        self.__date = datetime.datetime.now()
        self.__currency = currency
        self.__course = course
        self.__amount = amount

    @property
    def source(self):
        return self.__source
    
    @property
    def destination(self):
        return self.__destination
    
    @property
    def date(self) -> datetime.datetime:
        return self.__date

    @property
    def currency(self) -> str:
        return self.__currency
    
    @property
    def course(self) -> float:
        return self.__course
    
    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def base_currency(self):
        return self.source.bank.base_currency

    @property
    def base_amount(self) -> float:
        if self.__currency == self.base_currency:
            return self.__amount
        return self.__amount * self.__course


class TransactionPool:
    def __init__(self):
        self.__pool = dict()

    def get(self, transaction_id: str):
        if transaction_id in self.__pool:
            return self.__pool[transaction_id]
        return None

    def add(self, transaction_id: str, transaction: Transaction):
        if transaction_id in self.__pool:
            raise KeyError("Transaction name is not unique")
        self.__pool[transaction_id] = transaction
