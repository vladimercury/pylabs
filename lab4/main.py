from lab4.commands import *
from sys import stderr

bank = Bank()

commands = {
    "addacc": AddAccountCommand(bank),
    "addcl": AddClientCommand(bank),
    "cash": CountTotalCashCommand(bank),
    "client": ClientCommand(bank),
    "course": CourseCommand(bank),
    "listacc": BankListAccountsCommand(bank),
    "listcl": BankListClientsCommand(bank)
}

while True:
    parts = input().split()
    if len(parts):
        command, *args = parts
        if command not in commands:
            if command == "help":
                for key in sorted(commands.keys()):
                    print(key, commands[key].help())
            elif command == "exit":
                break
            else:
                print("%s: command not exists" % command)
        else:
            try:
                print(commands[command](*args))
            except CommandError as e:
                print("ERROR:", str(e), file=stderr)
