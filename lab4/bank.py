from lab4.account import Account, AccountPool
from lab4.client import Client, ClientPool


class Bank:
    @staticmethod
    def _generate_acc_id(start: int = 1):
        counter = start
        while True:
            yield "%05d" % counter
            counter += 1

    def __init__(self, base_currency: str = "RUR"):
        self.__account_pool = AccountPool()
        self.__account_id_generator = self._generate_acc_id()
        self.__base_currency = base_currency
        self.__client_pool = ClientPool()
        self.__courses = dict()

    def _generator(self):
        return self.__account_id_generator

    @property
    def base_currency(self):
        return self.__base_currency

    def get_all_accounts(self):
        accounts = self.__account_pool.get_accounts()
        return sorted(accounts, key=lambda x: x.id)

    def get_account(self, account_id):
        return self.__account_pool.get(account_id)

    def get_all_clients(self):
        clients = self.__client_pool.get_clients()
        return sorted(clients, key=lambda x: x.name)

    def get_client(self, client_name):
        return self.__client_pool.get(client_name)

    def get_total_cash(self):
        accounts = self.get_all_accounts()
        return sum([account.amount for account in accounts])

    def add_client(self, client_name: str):
        client = Client(client_name)
        self.__client_pool.add(client.name, client)
        return client.name

    def add_account(self, client_name: str, start_sum: float = 0.0):
        client = self.__client_pool.get(client_name)
        account = Account(next(self._generator()), client, self, start_sum)
        self.__account_pool.add(account.id, account)
        client.add_account(account)
        return account.id

    def get_course(self, currency):
        if currency not in self.__courses:
            return None
        return self.__courses[currency]

    def set_course(self, currency, value):
        self.__courses[currency] = value
