from utils import WebInput
import re
import os
from time import time


RE_ROW = re.compile(r'(?P<state>(on|off)) x=(?P<min_x>[-\d]+)\.\.(?P<max_x>[-\d]+),y=(?P<min_y>[-\d]+)\.\.(?P<max_y>[-\d]+),z=(?P<min_z>[-\d]+)\.\.(?P<max_z>[-\d]+)')  # noqa: E501





class DayInput(WebInput):
    def __init__(self, part=1, **kwargs):
        DAY = int(__file__.split(".")[0].split("_")[-1])
        super().__init__(day=DAY, **kwargs)
        self.grid = dict()
        self.part = part
        self.durations = []
        self.get_content()
        cnt_max = len(self.rows)
        # on x=10..12,y=10..12,z=10..12
        for i, row in enumerate(self.rows):
            start = time()
            matches = RE_ROW.match(row)
            state = 1 if matches.group("state") == "on" else 0
            try:
                for coord in self.range_xyz(matches):
                    if state == 1:
                        self.grid[coord] = 1.0
                    else:
                        try:
                            del self.grid[coord]
                        except KeyError:
                            pass
            except KeyError:
                pass
            self.durations.append(time() - start)
            os.system('clear')
            print(f"Progression={int(100 * i / cnt_max)}%")
            remaining = (sum(self.durations) / (i + 1)) * (cnt_max - i + 1)
            minutes = remaining // 60
            secondes = int(remaining % 60)
            print(f"Remaining time {minutes} min and {secondes} sec")

    def range_xyz(self, matches):
        min_x, max_x = self.get_in_range(matches.group("min_x"), matches.group("max_x"),)
        min_y, max_y = self.get_in_range(matches.group("min_y"), matches.group("max_y"))
        min_z, max_z = self.get_in_range(matches.group("min_z"), matches.group("max_z"))
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    yield (x, y, z)

    def get_in_range(self, value_min, value_max):
        value_min = int(value_min)
        value_max = int(value_max)
        if self.part == 2:
            return value_min, value_max
        if value_max < -50:
            raise KeyError('max_value inf to -50')
        elif value_min > 50:
            raise KeyError('max_value sup to 50')
        i = value_min if -50 <= value_min <= 50 else -50
        a = value_max if -50 <= value_max <= 50 else 50
        return (i, a)

    def count_on(self):
        cubes_on = [c for c in self.grid.values() if c.on]
        cnt = len(cubes_on)
        return cnt


test = True
input = DayInput(test=test, part=2)
print("Part two:", input.count_on())
