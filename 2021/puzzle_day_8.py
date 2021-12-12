from utils import WebInput
# import numpy as np


class DayInput(WebInput):
    def __init__(self, day=8, **kwargs):
        super().__init__(day=day, **kwargs)

    def count(self):
        total = 0
        for row in self.get_content():
            inputs, outputs = row.split("|")
            outputs = outputs.strip().split()
            count = [len(i) for i in outputs if len(i) in (2, 3, 4, 7)]
            total += len(count)
        return total

    def part_one(self):
        count = self.count()
        print(f"Part one: {count}")

    def analyse_inputs(self, inputs):
        """inputs = ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', ...]"""
        mapping = {i: None for i in range(10)}
        group_5 = [i for i in inputs if len(i) == 5]
        group_6 = [i for i in inputs if len(i) == 6]
        # find 1, 4, 7 and 8
        for input in inputs:
            if len(input) == 2:
                mapping[1] = input
            elif len(input) == 3:
                mapping[7] = input
            elif len(input) == 4:
                mapping[4] = input
            elif len(input) == 7:
                mapping[8] = input
        # find 2, 3 and 5
        for input in group_5:
            # find 2
            if len(set(mapping[4]) - set(input)) == 2:
                mapping[2] = input
            # find 3
            elif set(input).issuperset(set(mapping[7])):
                mapping[3] = input
            # find 5
            else:
                mapping[5] = input
        for input in group_6:
            if set(input).issuperset(set(mapping[3])):
                mapping[9] = input
            elif set(input).issuperset(set(mapping[7])):
                mapping[0] = input
            else:
                mapping[6] = input
        return {frozenset(v): k for k, v in mapping.items()}

    def analyze(self):
        total = 0
        for row in self.get_content():
            inputs, outputs = row.split("|")
            mapping = self.analyse_inputs(inputs.strip().split())
            outputs = outputs.strip().split()
            digit = [str(mapping[frozenset(d)]) for d in outputs]
            total += int("".join(digit))
        return total

    def part_two(self):
        total = self.analyze()
        print(f"Part two: {total}")


DayInput(test=False).part_two()
