from utils import WebInput

# name of the file must be something_[DAY].py where [DAY] can be 15, 16, 24...
DAY = int(__file__.split(".")[0].split("_")[-1])


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)

    def print(self):
        print()

    def part_one(self):
        total = 0
        print(f"Part one: {total}")

    def part_two(self):
        total = 0
        print(f"Part two: {total}")


test = True
DayInput(test=test).part_one()
DayInput(test=test).part_two()
