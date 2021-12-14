from utils import WebInput
from more_itertools import windowed
# from collections import Counter


class DayInput(WebInput):
    def __init__(self, day=14, **kwargs):
        super().__init__(day=day, **kwargs)
        self.polymer = dict()
        self.mapping = dict()
        self.count = dict()
        elts = set()
        for i, row in enumerate(self.get_content()):
            if i == 0:
                raw_polymer = row
            else:
                pair, elt = row.split(" -> ")
                self.mapping[pair] = {
                    "pairs": [
                        "".join([pair[0], elt]),
                        "".join([elt, pair[1]]),
                    ],
                    "elt": elt,
                }
                elts.add(elt)
        self.count = {e: 0 for e in elts}
        self.polymer = {k: 0 for k in self.mapping.keys()}
        for window in windowed(raw_polymer, 2):
            pair = "".join(window)
            self.polymer[pair] += 1
        for elt in raw_polymer:
            self.count[elt] += 1

    def loop(self):
        old_polymer = {k: v for k, v in self.polymer.items() if v > 0}
        self.polymer = {k: 0 for k in self.mapping.keys()}
        for pair, count in old_polymer.items():
            for new_pair in self.mapping[pair]["pairs"]:
                self.polymer[new_pair] += count
            elt = self.mapping[pair]["elt"]
            self.count[elt] += count
        if self.test:
            self.print()

    def print(self):
        print(self.count, sum(self.count.values()))

    def total(self):
        cnt = list(self.count.values())
        cnt.sort()
        return cnt[-1] - cnt[0]

    def part_one(self):
        self.print()
        for i in range(10):
            self.loop()
        print(f"Part one: {self.total()}")

    def part_two(self):
        self.print()
        for i in range(40):
            self.loop()
        print(f"Part two: {self.total()}")


test = False
DayInput(test=test).part_one()
DayInput(test=test).part_two()
