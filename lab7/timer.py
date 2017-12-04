import datetime


class Timer:
    @staticmethod
    def now():
        return datetime.datetime.now()

    def __init__(self):
        self.mark = self.now()

    def reset(self):
        self.mark = self.now()

    def diff(self):
        return self.now() - self.mark
