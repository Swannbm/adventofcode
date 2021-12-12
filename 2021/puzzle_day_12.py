from utils import WebInput, Cell
from collections import Counter


class DayCell(Cell):
    def __init__(self, name):
        self.name = name
        self.is_small = False
        if self.name.lower() == self.name or self.name in ["start", "end"]:
            self.is_small = True
        self.adjacents = []

    def add_connexion(self, cell):
        self.adjacents.append(cell)

    def get_next_cells(self, visited):
        cnt = Counter(s for s in visited if s.is_small)
        if len(cnt) == 0 or max(cnt.values()) == 1:
            # on a pas encore visité 2 fois une petite cave
            # on peut donc tout revisiter
            next_cells = [c for c in self.adjacents if c.name not in ["start"]]  # noqa: E501
        else:
            next_cells = [
                c for c in self.adjacents
                if not c.is_small or c not in visited
            ]
        return next_cells

    def out_going_paths(self, visited):
        # on est arrivé à la sortir
        if self.name == "end":
            return [[self], ]
        new_visited = visited.copy()
        new_visited.append(self)
        # c'est une grosse cave
        # ou elle n'a pas encore été visitée
        next_cells = self.get_next_cells(new_visited)
        # on est dans un cul de sac
        if not next_cells:
            return [[self], ]
        paths = []
        for cell in next_cells:
            for path in cell.out_going_paths(new_visited):
                paths.append([self] + path)
        return paths

    def __repr__(self):
        return self.name


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

    def find_paths(self):
        paths = self.start.out_going_paths(list())
        ending_paths = []
        for path in paths:
            if path[-1] == self.end:
                ending_paths.append(path)
                if self.test:
                    print(path)
        return len(ending_paths)

    def part_one(self):
        total = self.find_paths()
        print(f"Part one: {total}")

    def part_two(self):
        total = 0
        print(f"Part two: {total}")


DayInput(test=False).part_one()
