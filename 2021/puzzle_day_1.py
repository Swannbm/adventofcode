from utils import Input
from more_itertools import windowed


class Increasing(Input):
    def count_increasing_row(self):
        windows = list(windowed(self.get_int(), 2))
        good_windows = [(a, b) for a, b in windows if b > a]
        cpt = len(good_windows)
        return cpt

    def part2(self):
        windows = list(windowed(self.get_int(), 3))
        summed = []
        for triplet in windows:
            if len(triplet) == 3:
                summed.append(sum(triplet))
        windows = list(windowed(summed, 2))
        good_windows = [(a, b) for a, b in windows if b > a]
        cpt = len(good_windows)
        return cpt


input = Increasing(day=1)
increased = input.count_increasing_row()
print(f"Part one: {increased}")


print(f"Part two: {input.part2()}")
