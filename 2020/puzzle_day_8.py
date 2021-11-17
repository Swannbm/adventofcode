from utils import Input


class InfiniteLoopException(Exception):
    pass


class Instruction:
    accu = 0

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

    def switch(self):
        if self.instruction not in ["nop", "jmp"]:
            return False
        if self.instruction == "nop":
            self.instruction = "jmp"
        else:
            self.instruction = "nop"
        return True

    def __str__(self):
        return f"{self.index}: {self.instruction} {self.value}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def init(cls, switch_index=None):
        switch_done = True if switch_index is None else False
        instructions = list(Input(day=8).iter(cls))
        for i, inst in enumerate(instructions):
            if switch_done is False and i >= switch_index:
                if inst.switch():
                    switch_done = True
            inst.init_next(i, instructions)
        return instructions[0]

    @classmethod
    def run(cls, raise_exception=False, switch_index=None):
        inst = cls.init(switch_index=switch_index)
        cls.accu = inst.accumulate()
        while inst.next:
            inst = inst.next
            cls.accu += inst.accumulate()


try:
    Instruction.run()
except InfiniteLoopException:
    print(f"Part 1: {Instruction.accu}")

good_end = False
switch_index = 0
while good_end is False:
    try:
        Instruction.run(switch_index=switch_index)
        good_end = True
    except InfiniteLoopException:
        switch_index += 1

print(f"Part 2: {Instruction.accu}")
