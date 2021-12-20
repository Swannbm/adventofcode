from utils import WebInput


DAY = int(__file__.split(".")[0].split("_")[-1])


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        self.grid = dict()
        self.get_content()
        self.encoding = self.rows[0]
        self.default = '.'
        self.cnt_enhancement = 0
        for y, row in enumerate(self.rows[1:]):
            for x, c in enumerate(row):
                self.grid[(x, y)] = c

    def get_enhanced_pixel(self, x, y):
        pattern = ""
        for yy in range(y - 1, y + 2):
            for xx in range(x - 1, x + 2):
                coord = (xx, yy)
                try:
                    c = self.grid[coord]
                    pattern += '1' if c == "#" else '0'
                except KeyError:
                    cnt = self.cnt_enhancement % 2
                    pattern += '0' if cnt == 0 else '1'
        index = int(pattern, 2)
        new_c = self.encoding[index]
        return new_c

    def get_min_max(self):
        min_x = min_y = max_x = max_y = 0
        for x, y in self.grid.keys():
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                yield (x, y)

    def enhance(self):
        new_grid = dict()
        for coord in self.get_min_max():
            new_grid[coord] = self.get_enhanced_pixel(*coord)
        self.grid = new_grid
        self.cnt_enhancement += 1

    def print(self):
        prev = None
        for coord in self.get_min_max():
            if coord[1] != prev:
                print()
            try:
                print(self.grid[coord], end="")
            except KeyError:
                print('.', end='')
            prev = coord[1]
        print()

    def count_ligth(self):
        cnt = 0
        for coord in self.get_min_max():
            try:
                if self.grid[coord] == '#':
                    cnt += 1
            except KeyError:
                pass
        return cnt

    def part_one(self):
        for i in range(2):
            if self.test:
                self.print()
            self.enhance()
        if self.test:
            self.print()
        print(f"Part one: {self.count_ligth()}")

    def part_two(self):
        for i in range(50):
            if self.test:
                self.print()
            self.enhance()
        if self.test:
            self.print()
        print(f"Part one: {self.count_ligth()}")


test = False
input = DayInput(test=test)
input.part_two()
# DayInput(test=test).part_two()
