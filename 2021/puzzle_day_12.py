from utils import WebInput, Cell


class DayCell(Cell):
    def __init__(self, name):
        self.name = name
        self.is_small = False
        if self.name.lower == self.name:
            self.is_small = True
        self.adjacents = None

    def add_connexion(self, cell):
        self.adjacents.append(cell)


class DayInput(WebInput):
    def __init__(self, day=12, **kwargs):
        super().__init__(day=day, **kwargs)
        self.cells = dict()
        for row in self.get_content():
            cell_1, cell_2 = [self.get_cell(n) for n in row.split("-")]
            cell_1.add_connexion(cell_2)
            cell_2.add_connexion(cell_1)
        self.start = self.cells["start"]
        self.end = self.cells["end"]

    def get_cell(self, name):
        if name not in self.cells.keys():
            self.cells[name] = DayCell(name)
        return self.cells[name]

    def part_one(self):
        total = 0
        print(f"Part one: {total}")

    def part_two(self):
        total = 0
        print(f"Part two: {total}")


DayInput(test=True).part_one()
