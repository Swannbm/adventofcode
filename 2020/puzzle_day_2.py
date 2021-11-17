from utils import Input


class Processor:
    def __init__(self, row):
        data = row.split()
        numbers = data[0].split("-")
        self.min = int(numbers[0])
        self.max = int(numbers[1])
        self.letter = data[1]
        self.password = data[2]

    def process(self):
        cpt = len(self.password.split(self.letter))
        if self.min <= cpt <= self.max:
            return 1
        else:
            return 0


input = Input(day=2)
cpt = sum(_.process() for _ in input.iter(Processor))
print(cpt)
