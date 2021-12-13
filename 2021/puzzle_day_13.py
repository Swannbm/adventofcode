from utils import WebInput, Cell


class DayCell(Cell):
    def get_folded_coord(self, direction, position):
        new_y = self.y
        new_x = self.x
        if direction == "x":
            new_x = position - (self.x - position)
        else:
            new_y = position - (self.y - position)
        return (new_x, new_y)

    def fold(self, cell):
        self.value |= cell.value


class DayInput(WebInput):
    def __init__(self, day=13, **kwargs):
        super().__init__(day=day, **kwargs)
        self.cells = dict()
        self.folding_orders = []
        self.max_x = self.max_y = 0
        for row in self.get_content():
            if row.startswith("fold along "):
                row = row.replace("fold along ", "")
                direction, position = row.split("=")
                self.folding_orders.append({
                    "direction": direction,
                    "position": int(position),
                })
            elif row:
                x, y = [int(i) for i in row.split(",")]
                self.cells[(x, y)] = DayCell(x, y, True)
                self.max_x = max(x + 1, self.max_x)
                self.max_y = max(y + 1, self.max_y)
        for x in range(self.max_x):
            for y in range(self.max_y):
                if (x, y) not in self.cells:
                    self.cells[(x, y)] = DayCell(x, y, False)

    def fold_y(self, position):
        """
        . Supprimer les cellules sur la ligne de fold.
        . Plier chaque cellule
        """
        # supprimer les cellules sur le pliage
        for x in range(self.max_x):
            del self.cells[(x, position)]
        # folder les cellules sous le pliage
        for y in range(position + 1, self.max_y):
            for x in range(self.max_x):
                new_c = self.cells[(x, y)].get_folded_coord("y", position)
                self.cells[new_c].fold(self.cells[(x, y)])
                del self.cells[(x, y)]
        self.max_y = position

    def fold_x(self, position):
        """
        . Supprimer les cellules sur la ligne de fold.
        . Plier chaque cellule
        """
        # supprimer les cellules sur le pliage
        for y in range(self.max_y):
            del self.cells[(position, y)]
        # folder les cellules sous le pliage
        for x in range(position + 1, self.max_x):
            for y in range(self.max_y):
                new_c = self.cells[(x, y)].get_folded_coord("x", position)
                self.cells[new_c].fold(self.cells[(x, y)])
                del self.cells[(x, y)]
        self.max_x = position

    def fold_once(self):
        order = self.folding_orders.pop(0)
        self.fold(order)

    def fold_all(self):
        for order in self.folding_orders:
            self.fold(order)

    def fold(self, order):
        if order["direction"] == "x":
            self.fold_x(order["position"])
        else:
            self.fold_y(order["position"])
        if self.test:
            self.print()

    def print(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.cells[(x, y)].value:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()

    def part_one(self):
        if self.test:
            self.print()
        self.fold_once()
        points = [c for c in self.cells.values() if c.value]
        total = len(points)
        print(f"Part one: {total}")

    def part_two(self):
        self.fold_all()
        print("Part two:")
        self.print()


test = False
# DayInput(test=test).part_one()
DayInput(test=test).part_two()
