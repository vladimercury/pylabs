from lab4v2.transaction import Transaction
from lab4v2.account import Account
from lab4v2.client import Client
from random import randint


class BankError(Exception):
    def __init__(self, message):
        super(BankError, self).__init__(message)


class Bank:
    class AccountRecord:
        def __init__(self, account: Account, owner: Client):
            self.__account = account
            self.__owner = owner
            self.__history = list()

        @property
        def account(self):
            return self.__account

        @property
        def owner(self):
            return self.__owner

        @property
        def history(self):
            return self.__history

        def add_transaction(self, transaction: Transaction):
            self.__history.append(transaction)

    class ClientRecord:
        def __init__(self, client: Client):
            self.__client = client
            self.__accounts = dict()

        @property
        def client(self) -> Client:
            return self.__client

        @property
        def accounts(self) -> list:
            return self.__accounts.items()

        def add_account(self, account: Account) -> None:
            if account.id in self.__accounts:
                raise BankError("Account with id '%s' already added to '%s'" % (account.id, self.__client.name))
            if account.owner.name != self.__client.name:
                raise BankError("Account owner doesn't match given client")
            self.__accounts[account.id] = account

        def has_account(self, account_id: str) -> bool:
            return account_id in self.__accounts

    @classmethod
    def get_id_generator(cls, n_digits: int = 10):
        while True:
            yield "%0*d" % (n_digits, randint(0, 10 ** n_digits))

    def __init__(self, base_currency: str = 'RUR', id_len: int = 5):
        self.__accounts = dict()
        self.__base_currency = base_currency
        self.__clients = dict()
        self.__rates = dict()
        self.__generator = self.get_id_generator(id_len)

    @property
    def base_currency(self):
        return self.__base_currency

    def _get_account_record(self, account_id: str) -> AccountRecord:
        account_id = account_id.upper()
        if account_id not in self.__accounts:
            raise BankError("Account with id '%s' not found" % account_id)
        return self.__accounts[account_id]

    def _get_client_record(self, client_name: str) -> ClientRecord:
        if client_name not in self.__clients:
            raise BankError("Client with name '%s' not found" % client_name)
        return self.__clients[client_name]

    def _generate_id(self, currency: str) -> str:
        while True:
            account_id = currency + next(self.__generator)
            if account_id not in self.__accounts:
                return account_id

    def add_account(self, owner_name: str, currency: str, start_cash: float = None):
        currency = currency.upper()
        if start_cash is None:
            start_cash = 0.0
        owner_record = self._get_client_record(owner_name)
        account_id = self._generate_id(currency)
        account = Account(self, account_id, currency, start_cash)
        record = Bank.AccountRecord(account, owner_record.client)
        self.__accounts[account_id] = record
        owner_record.add_account(account)
        return account

    def add_client(self, client_name: str):
        if client_name in self.__clients:
            raise BankError("Client with name '%s' already exists" % client_name)
        client = Client(self, client_name)
        record = Bank.ClientRecord(client)
        self.__clients[client_name] = record
        return client

    def count_full_cash(self):
        return sum((record.account.base_currency_cash for record in self.__accounts.values()))

    def do_transaction(self, src_owner: Client, src_id: str, dst_id: str, cash: float, currency: str = None):
        src_record = self._get_account_record(src_id)
        dst_record = self._get_account_record(dst_id)
        if src_record.owner.name != src_owner.name:
            raise BankError("Client '%s' is not an account '%s' owner" % (src_owner.name, src_id))
        if currency is None:
            currency = src_record.account.currency
        exchange_rate = self.get_exchange_rate(currency)
        base_cash = exchange_rate * cash
        if base_cash > src_record.account.base_currency_cash:
            raise BankError("Not enough money")
        src_record.account.base_currency_cash -= base_cash
        dst_record.account.base_currency_cash += base_cash
        transaction = Transaction(self, src_id, dst_id, cash, currency, exchange_rate)
        src_record.add_transaction(transaction)
        dst_record.add_transaction(transaction)
        return transaction, src_record.account

    def get_all_accounts(self) -> list:
        return [(record.account, record.owner) for acc_id, record in sorted(self.__accounts.items())]

    def get_account(self, account_id: str):
        return self._get_account_record(account_id).account

    def get_account_cash(self, client: Client, account_id: str):
        record = self._get_account_record(account_id)
        if record.owner.name != client.name:
            raise BankError("Client '%s' is not an account '%s' owner" % (client.name, account_id))
        account = record.account
        return account.cash, account.currency, account.base_currency_cash, self.base_currency

    def get_account_owner(self, account: Account):
        return self._get_account_record(account.id).owner

    def get_account_transaction_history(self, account: Account):
        return self._get_account_record(account.id).history

    def get_client(self, client_id: str):
        return self._get_client_record(client_id).client

    def get_client_accounts(self, client: Client):
        return self._get_client_record(client.name).accounts

    def get_exchange_rate(self, currency: str):
        currency = currency.upper()
        if currency not in self.__rates:
            if currency == self.base_currency:
                return 1.0
            raise BankError("Exchange rate for '%s' not provided" % currency)
        return self.__rates[currency]

    def list_accounts(self) -> list:
        return [record.account for acc_id, record in self.__accounts.items()]

    def set_exchange_rate(self, currency: str, value: float):
        if value <= 0.0:
            raise BankError("Exchange rate is zero or negative")
        self.__rates[currency.upper()] = value