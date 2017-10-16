from lab4.transaction import Transaction


class Account:
    def __init__(self, identifier, client, bank, start_amount: float = 0.0):
        self.__id = identifier
        self.__client = client
        self.__bank = bank
        self.__amount = start_amount
        self.__history = []

    @property
    def id(self):
        return self.__id

    @property
    def client(self):
        return self.__client

    @property
    def bank(self):
        return self.__bank

    @property
    def amount(self):
        return self.__amount

    @property
    def transaction_history(self):
        return self.__history

    def _get_course(self, currency: str) -> float:
        return self.bank.get_course(currency)

    def send_cash(self, destination, amount: float, currency: str = None):
        self._withdraw(destination, amount, currency)
        destination.deposit(self, amount, currency)

    def _withdraw(self, destination, amount: float, currency: str = None):
        if currency is None:
            currency = self.bank.base_currency
        course = self._get_course(currency)
        self.__amount -= amount * course
        self.__history.append(Transaction(self, destination, amount, currency, course))

    def deposit(self, source, amount: float, currency: str = None):
        if currency is None:
            currency = self.bank.base_currency
        course = self._get_course(currency)
        self.__amount += amount * course
        self.__history.append(Transaction(source, self, amount, currency, course))


class AccountPool:
    def __init__(self):
        self.__pool = dict()

    def get_ids(self):
        return self.__pool.keys()

    def get_accounts(self):
        return self.__pool.values()

    def get(self, account_id: str):
        return self.__pool[account_id]

    def add(self, account_id: str, account: Account):
        if account_id in self.__pool:
            raise KeyError("Account ID is not unique")
        self.__pool[account_id] = account
