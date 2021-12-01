from utils import Input
from more_itertools import windowed


class Increasing(Input):
    def count_increasing_row(self):
        increase = 0
        rows = self.get_content()
        for i in range(1, len(rows)):
            if rows[i - 1] < rows[i]:
                increase += 1
        return increase

    def window(self):
        windows = list(windowed(self.get_content(), 2))
        return windows


input = Increasing(day=1)
increased = input.count_increasing_row()
print(f"Part one: {increased}")

windows = input.window()
good_windows = [(a, b) for a, b in windows if b > a]
cpt = len(good_windows)

print(cpt)
