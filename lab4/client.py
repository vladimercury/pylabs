class Client:
    def __init__(self, name: str):
        self.__name = name
        self.__accounts = list()

    @property
    def name(self) -> str:
        return self.__name


class ClientPool:
    def __init__(self):
        self.__pool = dict()

    def get(self, client_name: str):
        if client_name in self.__pool:
            return self.__pool[client_name]
        return None

    def add(self, client_name: str, client: Client):
        if client_name in self.__pool:
            raise KeyError("Client name is not unique")
        self.__pool[client_name] = client


