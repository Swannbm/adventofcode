from utils import Input


input = Input(day=2)


class ProcessorPartOne:
    def __init__(self, row):
        data = row.split()
        numbers = data[0].split("-")
        self.min = int(numbers[0])
        self.max = int(numbers[1])
        self.letter = data[1].replace(":", "")
        self.password = data[2]

    def count(self):
        cpt = 0
        for c in self.password:
            if c == self.letter:
                cpt += 1
        return cpt

    def process(self):
        if self.min <= self.count() <= self.max:
            return 1
        else:
            return 0


cpt = sum(_.process() for _ in input.iter(ProcessorPartOne))
print(f"Part 1: {cpt}")


class ProcessorPartTow(ProcessorPartOne):
    def process(self):
        cpt = 0
        if self.password[self.min - 1] == self.letter:
            cpt += 1
        if self.password[self.max - 1] == self.letter:
            cpt += 1
        return 1 if cpt == 1 else 0


cpt = sum(_.process() for _ in input.iter(ProcessorPartTow))
print(f"Part 2: {cpt}")
