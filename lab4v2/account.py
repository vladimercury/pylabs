class Account:
    def __init__(self, bank, account_id: str, currency: str, start_cash: float = 0.0):
        self.__bank = bank
        self.__id = account_id
        self.__currency = currency
        self.__cash = start_cash

    @property
    def id(self):
        return self.__id

    @property
    def currency(self):
        return self.__currency

    @property
    def cash(self):
        return self.__cash

    @cash.setter
    def cash(self, value):
        self.__cash = value

    @property
    def base_currency_cash(self):
        exchange_rate = self.__bank.get_exchange_rate(self.__currency)
        return exchange_rate * self.__cash

    @base_currency_cash.setter
    def base_currency_cash(self, value):
        exchange_rate = self.__bank.get_exchange_rate(self.__currency)
        self.__cash = value / exchange_rate

    @property
    def owner(self):
        return self.__bank.get_account_owner(self)

    @property
    def transaction_history(self):
        return self.__bank.get_account_transaction_history(self)

    def __str__(self):
        return "Account %s: %.2f %s" % (self.__id, self.__cash, self.__currency)