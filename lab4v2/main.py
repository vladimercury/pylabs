from lab4v2.bank import Bank, BankError
from sys import stderr


class CommandError(Exception):
    def __init__(self, message):
        super(CommandError, self).__init__(message)

bank = Bank(id_len=3)
context = None


def check_context():
    if context is None:
        raise CommandError("Client context not set")


def add_account(owner_name, currency, *args):
    """owner_name:str, currency:str, [start_cash:float]\n\tCreates new account"""
    start_cash = float(args[0].replace(",", ".")) if len(args) else None
    account = bank.add_account(owner_name, currency, start_cash)
    print("Added account with ID '%s'" % account.id)


def add_client(client_name, *args):
    """client_name:str\n\tCreates new client"""
    client = bank.add_client(client_name)
    print("Added client with name '%s'" % client.name)


def bank_or_account_cash(*args):
    """[account_id:str]\n\tCount cash in bank or in context client's account"""
    account_id = args[0] if len(args) else None
    if account_id is None:
        print("Total cash is %.2f %s" % (bank.count_full_cash(), bank.base_currency))
    else:
        if context is None:
            raise CommandError("Client context not set")
        cash, currency, base_cash, base_currency = context.get_account_cash(account_id)
        if base_currency == currency:
            print("%.2f %s" % (cash, currency))
        else:
            print("%.2f %s (%.2f %s)" % (cash, currency, base_cash, base_currency))


def client_info(*args):
    """\n\tShow context client info"""
    check_context()


def get_or_set_context(*args):
    """[client_name:str]\n\tGet pr set client context"""
    global context
    client_name = args[0] if len(args) else None
    if client_name is None:
        check_context()
        print("Client '%s': %.2f %s" % context.info)
    else:
        context = bank.get_client(client_name)
        print("Client context set to '%s'" % context.name)


def get_or_set_exchange_rate(currency, *args):
    """currency:str [value:float]\n\tGet or set exchange rate"""
    value = float(args[0].replace(",", ".")) if len(args) else None
    if value is None:
        value = bank.get_exchange_rate(currency)
        print("Exchange rate for '%s' is %.8f" % (currency, value))
    else:
        bank.set_exchange_rate(currency, value)
        print("Exchange rate for '%s' set to %.8f" % (currency, value))


def exit_bank(*args):
    """\n\tExit bank"""
    print("Exiting bank...")
    exit(0)


def list_accounts(*args):
    """\n\tList all bank accounts"""
    for account, owner in bank.get_all_accounts():
        print(str(account), "/ Owner:", owner.name)


def send_cash(src_id, dst_id, cash, *args):
    """source_id:str, destination_id:str, cash:float, [currency:str]\n\tSend cash"""
    check_context()
    cash = float(cash.replace(",", "."))
    currency = args[0] if len(args) else None
    transaction, account = context.send(src_id, dst_id, cash, currency)
    print(str(transaction))
    print("Account '%s' cash is %.2f %s" % (account.id, account.cash, account.currency))


def show_transaction_history(*args):
    """[account_id:str]\n\tShow transaction history for bank/account"""
    account_id = args[0] if len(args) else None
    history = list()
    if account_id is None:
        history = bank.history
    else:
        check_context()
        history = context.get_account_history(account_id)
    for transaction in history:
        print(str(transaction))
    if len(history) == 0:
        print("No transactions")

commands = {
    "ca": add_account,
    "cash": bank_or_account_cash,
    "exit": exit_bank,
    "cc": add_client,
    "list": list_accounts,
    "rate": get_or_set_exchange_rate,
    "me": get_or_set_context,
    "send": send_cash,
    "hist": show_transaction_history
}

for command, func in sorted(commands.items()):
    print(command, func.__doc__)
print()
while True:
    words = input().split()
    if len(words) > 0:
        command, *arguments = words
        if command in commands:
            try:
                commands[command](*arguments)
            except ValueError or TypeError:
                print("Invalid argument list", file=stderr)
            except BankError as be:
                print(be, file=stderr)
            except CommandError as ce:
                print(ce, file=stderr)
        else:
            print("Command not found", file=stderr)
