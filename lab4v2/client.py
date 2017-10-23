class Client:
    def __init__(self, bank, name: str):
        self.__bank = bank
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def accounts(self):
        return self.__bank.get_client_accounts(self)

    def get_account_cash(self, account_id: str):
        return self.__bank.get_account_cash(self, account_id)

    def send(self, src_id: str, dst_id: str, cash: float, currency: str = None):
        return self.__bank.do_transaction(self, src_id, dst_id, cash, currency)

