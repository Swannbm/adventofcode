from utils import Input


class InfiniteLoopException(Exception):
    pass


class Instruction:
    def __init__(self, row):
        """
            nop +0
            acc +1
            jmp +4
            acc +3
            jmp -3
            acc -99
            acc +1
            jmp -4
            acc +6
        """
        self.done = False
        self.instruction, value = row.split()
        self.value = int(value)
        self.index = None
        self.next_index = None
        self.next = None

    def init_next(self, current_index, instructions):
        try:
            self.index = current_index
            if self.instruction in ["nop", "acc"]:
                self.next_index = current_index + 1
            elif self.instruction == "jmp":
                self.next_index = current_index + self.value
            self.next = instructions[self.next_index]
        except IndexError:
            pass

    def accumulate(self):
        if self.done is True:
            raise InfiniteLoopException()
        self.done = True
        if self.instruction == "acc":
            return self.value
        return 0

    def __str__(self):
        return f"{self.index}: {self.instruction} {self.value}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def init(cls):
        instructions = list(Input(day=8).iter(cls))
        for i, inst in enumerate(instructions):
            inst.init_next(i, instructions)
        return instructions[0]

    @classmethod
    def run(cls, raise_exception=False):
        inst = cls.init()
        accu = 0
        while inst.next:
            inst = inst.next
            accu += inst.accumulate()
            yield accu


accu = 0
try:
    for accu in Instruction.run():
        pass
except InfiniteLoopException:
    print(f"Part 1: {accu}")

accu = 0

print(f"Part 2: {accu}")
