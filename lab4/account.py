class Account:
    def __init__(self, client, bank, start_amount: float = 0.0):
        self.__client = client
        self.__bank = bank
        self.__amount = start_amount

    @property
    def client(self):
        return self.__client

    @property
    def bank(self):
        return self.__bank

    def send_cash(self, account, amount: float, currency):
        self._withdraw(amount, currency)
        account.deposit(amount, currency)

    def _withdraw(self, amount: float, currency: str):
        self.__amount -= amount * self.bank.get_course(currency)

    def deposit(self, amount: float, currency: str):
        self.__amount += amount * self.bank.get_course(currency)

    def get_amount(self):
        pass

    def get_transact_history(self):
        pass


class AccountPool:
    def __init__(self):
        self.__pool = dict()

    def get(self, account_id: str):
        if account_id in self.__pool:
            return self.__pool[account_id]
        return None

    def add(self, account_id: str, account: Account):
        if account_id in self.__pool:
            raise KeyError("Account ID is not unique")
        self.__pool[account_id] = account
