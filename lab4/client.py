from lab4.account import Account, AccountPool


class Client:
    def __init__(self, name: str):
        self.__name = name
        self.__account_pool = AccountPool()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def accounts(self) -> list:
        return self.__account_pool.get_ids()

    def add_account(self, account: Account):
        if account.client != self:
            raise ValueError("Client does not match")
        self.__account_pool.add(account.id, account)

    def get_total_cash(self) -> float:
        return sum([account.amount for account in self.__account_pool.get_accounts()])

    def get_account_cash(self, account_id: str) -> float:
        account = self.__account_pool.get(account_id)
        return account.amount

    def send_cash(self, source_id: str, destination, amount: float, currency: str = None):
        source = self.__account_pool.get(source_id)
        if amount > source.amount:
            raise ValueError("Not enough money")
        source.send_cash(destination, amount, currency)

    def get_account_transaction_history(self, account_id: str):
        account = self.__account_pool.get(account_id)
        return account.transaction_history


class ClientPool:
    def __init__(self):
        self.__pool = dict()

    def get(self, client_name: str):
        return self.__pool[client_name]

    def add(self, client_name: str, client: Client):
        if client_name in self.__pool:
            raise KeyError("Client name is not unique")
        self.__pool[client_name] = client

    def get_clients(self):
        return self.__pool.values()
