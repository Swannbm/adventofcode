from utils import WebInput


class DayInput(WebInput):
    def __init__(self, day=14, **kwargs):
        super().__init__(day=day, **kwargs)

    def part_one(self):
        total = 0
        print(f"Part one: {total}")

    def part_two(self):
        total = 0
        print(f"Part two: {total}")


DayInput.init(14)

DayInput(test=True).part_one()
