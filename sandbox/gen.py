class Generators:
    @staticmethod
    def natural_numbers(next_val=1):
        counter = next_val
        while True:
            change = (yield counter)
            if change is None:
                counter += 1
            else:
                counter = change

gen = Generators.natural_numbers()
for _ in range(10):
    print(next(gen), end=' ')
    print()
gen.send(1002314)
for _ in range(10):
    print(next(gen), end=' ')
    print()
