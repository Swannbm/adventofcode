from utils import WebInput
# import numpy as np


PATTERNS = ["[]", "()", "{}", "<>"]
BRACKETS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
CLOSING = {v: k for k, v in BRACKETS.items()}
POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
POINTS_COMPLETION = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


class DayInput(WebInput):
    def __init__(self, day=10, **kwargs):
        super().__init__(day=day, **kwargs)

    def clean(self):
        new_content = self.get_raw_content()
        prev_content = ""
        while prev_content != new_content:
            prev_content = new_content
            for needle in PATTERNS:
                new_content = new_content.replace(needle, "")
            if self.test:
                print(new_content)
                print()

    def check(self):
        total_corrupted = 0
        total_completion = []
        for row in self.get_content():
            try:
                total = self.check_line(row)
                print(f"Completing: => {total}")
                total_completion.append(total)
            except Exception as e:
                c = e.char
                if self.test:
                    print(f"Corrupted: {c} => {POINTS[c]}")
                total_corrupted += POINTS[c]
        total_completion.sort()
        index = int(len(total_completion) / 2)
        return total_corrupted, total_completion[index]

    def check_line(self, row):
        chain = []
        for c in row:
            if c in BRACKETS.keys():
                chain.append(c)
            else:  # '(' ')'
                if chain[-1] == CLOSING[c]:
                    chain.pop()
                else:
                    e = Exception("corrupted")
                    e.char = c
                    raise e
        total = 0
        closing_chain = [BRACKETS[c] for c in chain[::-1]]
        for c in closing_chain:
            total *= 5
            total += POINTS_COMPLETION[c]
        return total

    def part_one(self):
        total_corrupted, total_completion = self.check()
        print(f"Part one: {total_corrupted}")
        print(f"Part two: {total_completion}")

    def part_two(self):
        total = self.check()
        print(f"Part two: {total}")


DayInput(test=False).part_one()
