from lab4.bank import Bank


class CommandError(Exception):
    def __init__(self, message):
        super(CommandError, self).__init__(message)


class Command:
    __client = None

    @classmethod
    def get_client(cls):
        return cls.__client

    @classmethod
    def set_client(cls, client):
        cls.__client = client

    def __init__(self, bank: Bank):
        self.__bank = bank

    @property
    def bank(self):
        return self.__bank

    def help(self):
        return ""

    def __call__(self, *args, **kwargs):
        return ""


class BankListAccountsCommand(Command):
    def help(self):
        return "\n\tList all bank accounts and clients they assigned to"

    def __call__(self, *args, **kwargs):
        lines = []
        accounts = self.bank.get_all_accounts()
        if len(accounts):
            for account in accounts:
                data = (account.id, account.client.name, account.amount, self.bank.base_currency)
                lines.append("%s: %s; %.2f %s" % data)
            return "\n".join(lines)
        return "No accounts"


class BankListClientsCommand(Command):
    def help(self):
        return "\n\tList all bank clients and their accounts"

    def __call__(self, *args, **kwargs):
        lines = []
        clients = self.bank.get_all_clients()
        if len(clients):
            for client in clients:
                lines.append("%s: %.2f %s" % (client.name, client.get_total_cash(), self.bank.base_currency))
            return "\n".join(lines)
        return "No clients"


class CountTotalCashCommand(Command):
    def help(self):
        return "\n\tCount total cash in bank"

    def __call__(self, *args, **kwargs):
        accounts = self.bank.get_all_accounts()
        cash = sum([account.amount for account in accounts])
        return str("Total cash is %.2f %s" % (cash, self.bank.base_currency))


class AddAccountCommand(Command):
    def help(self):
        return "CLIENT_NAME [START_CASH]\n\tAdd account to bank"

    def __call__(self, *args, **kwargs):
        if len(args):
            name = args[0]
            start_cash = 0.0
            if len(args) > 1:
                try:
                    start_cash = float(args[1])
                except ValueError:
                    raise CommandError("Start cash is not a number")
            try:
                acc_id = self.bank.add_account(name, start_cash)
                return "Created account with id %s" % acc_id
            except KeyError:
                raise CommandError("Client with given name not exists")
        else:
            raise CommandError("Client name not provided")


class AddClientCommand(Command):
    def help(self):
        return "CLIENT_NAME\n\tAdd client to bank"

    def __call__(self, *args, **kwargs):
        if len(args):
            try:
                name = self.bank.add_client(args[0])
                return "Created client with name %s" % name
            except KeyError:
                raise CommandError("Client with given name already exists")
        else:
            raise CommandError("Client name not provided")


class ClientCommand(Command):
    def help(self):
        return "[CLIENT_NAME]\n\tSet or get current client"

    def __call__(self, *args, **kwargs):
        if len(args):
            try:
                self.__class__.set_client(self.bank.get_client(args[0]))
                return "Client set to %s" % args[0]
            except KeyError:
                raise CommandError("Client with given name already exists")
        else:
            client = self.__class__.get_client()
            if client is None:
                return "Current client not set"
            else:
                return "Current client is %s" % client.name


class CourseCommand(Command):
    def help(self):
        return "CURRENCY [NEW_COURSE]\n\tGet or set course for currency"

    def __call__(self, *args, **kwargs):
        if len(args):
            currency_code = args[0]
            if len(args) > 1:
                try:
                    new_course = float(args[1])
                    self.bank.set_course(currency_code, new_course)
                    return "Course for %s set successfully" % currency_code
                except ValueError:
                    raise CommandError("New course is not a number")
            else:
                course = self.bank.get_course(currency_code)
                if course is None:
                    return "Course for %s not set" % currency_code
                return "1 %s = %f %s" % (currency_code, course, self.bank.base_currency)
        else:
            raise CommandError("Currency name not provided")


class SendMoneyCommand(Command):
    def help(self):
        return "ACCOUNT_ID AMOUNT [CURRENCY]\n\tSend money to another account"

    def __call__(self, *args, **kwargs):
        pass