from lab4.bank import Bank

command_client = None


class CommandError(Exception):
    def __init__(self, message):
        super(CommandError, self).__init__(message)


class Command:
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
                global command_client
                command_client = self.bank.get_client(args[0])
                return "Client set to %s" % args[0]
            except KeyError:
                raise CommandError("Client with given name already exists")
        else:
            client = command_client
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
        return "SOURCE_ACC DEST_ACC AMOUNT [CURRENCY]\n\tSend money to another account"

    def __call__(self, *args, **kwargs):
        if len(args) > 2:
            source, dest, amount, *currency = args
            client = command_client
            if client is None:
                raise CommandError("Current client is not set")
            try:
                source_acc = self.bank.get_account(source)
                dest_acc = self.bank.get_account(dest)
                amount_val = float(amount)
            except KeyError:
                raise CommandError("Account not found")
            except ValueError as e:
                raise CommandError("Amount is not a number")
            currency_name = currency[0] if len(currency) else None
            if source_acc.id not in client.accounts:
                raise CommandError("Current client is not source account owner")
            try:
                source_acc.send_cash(dest_acc, amount_val, currency_name)
            except ValueError as e:
                raise CommandError(str(e))
            return ""
        else:
            raise CommandError("Invalid argument list")


class ShowCashCommand(Command):
    def help(self):
        return "ACCOUNT_ID\n\tShow cash for account"

    def __call__(self, *args, **kwargs):
        if len(args):
            account_id, *extra = args
            try:
                account = self.bank.get_account(account_id)
            except KeyError:
                raise CommandError("Account not found")
            if command_client is None:
                raise CommandError("Current client not set")
            if account_id not in command_client.accounts:
                raise CommandError("Current client is not account owner")
            return "%.2f %s" % (account.amount, self.bank.base_currency)
        else:
            raise CommandError("Account id not provided")


class ShowTransactionHistoryCommand(Command):
    def help(self):
        return "ACCOUNT_ID\n\tShow transaction history for account"

    def __call__(self, *args, **kwargs):
        if len(args):
            account_id, *extra = args
            try:
                account = self.bank.get_account(account_id)
            except KeyError:
                raise CommandError("Account not found")
            if command_client is None:
                raise CommandError("Current client not set")
            if account_id not in command_client.accounts:
                raise CommandError("Current client is not account owner")
            lines = []
            for transaction in account.transaction_history:
                line = "%s -> %s: %.2f %s at %s"
                line_args = (transaction.source.id, transaction.destination.id, transaction.amount,
                             transaction.currency, transaction.date)
                if transaction.currency != transaction.base_currency:
                    line += " with 1 %s = %.6f %s (%.2f %s total)"
                    line_args = line_args + (transaction.currency, transaction.course, transaction.base_currency,
                                             transaction.amount * transaction.course, transaction.base_currency)
                lines.append(line % line_args)
            return "\n".join(lines)
        else:
            raise CommandError("Account id not provided")