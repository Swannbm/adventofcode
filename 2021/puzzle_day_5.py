from utils import WebInput
from pandas import DataFrame


def get_coordinates(row):
    a, b = row.split(' -> ')
    x1, y1 = [int(_) for _ in a.split(",")]
    x2, y2 = [int(_) for _ in b.split(",")]
    return x1, y1, x2, y2


class Map(WebInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        r = 10
        if not self.test:
            r = 991
        self.map = DataFrame(index=range(r), columns=range(r))
        self.map = self.map.fillna(0)
        self.part = 1

    def trace(self, x1, y1, x2, y2):
        if x1 == x2:
            if y1 < y2:
                points = [(x1, y) for y in range(y1, y2+1)]
            else:
                points = [(x1, y) for y in range(y2, y1+1)]
        elif y1 == y2:
            if x1 < x2:
                points = [(x, y1) for x in range(x1, x2+1)]
            else:
                points = [(x, y1) for x in range(x2, x1+1)]
        else:
            points = self.trace_diagonal(x1, y1, x2, y2)

        for x, y in points:
            value = self.map.at[y, x]
            self.map.at[y, x] = value + 1

    def trace_diagonal(self, x1, y1, x2, y2):
        if self.part == 1:
            return []
        if abs(x1 - x2) != abs(y1 - y2):
            return []
        points = []
        for i in range(abs(x1 - x2)+1):
            x = x1 + (i if x1 < x2 else -i)
            y = y1 + (i if y1 < y2 else -i)
            points.append((x, y))
        return points

    def get_map(self):
        for row in self.get_content():
            self.trace(*get_coordinates(row))
            if self.test:
                print(row)
                print(self.map)
                print()

    def part_one(self):
        self.get_map()
        total = self.map[self.map > 1].count()
        total = total.sum()
        print(f"Part one: {total}")
        return total

    def part_two(self):
        self.part = 2
        self.part_one()


Map(
    day=5,
    # test=True,
).part_two()
