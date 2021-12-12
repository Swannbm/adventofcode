from utils import WebInput
# import numpy as np


class Cell:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.adjacents = []
        self.bassin_center = None
        self.bassin_size = 0

    def set_adjacents(self, cells):
        adjacents = [
            (-1, 0),  # gauche
            (1, 0),  # droite
            (0, -1),  # haut
            (0, 1),  # bas
        ]
        for i, j in adjacents:
            pos = (self.x + i, self.y + j)
            if pos in cells.keys():
                self.adjacents.append(cells[pos])

    def is_low_point(self):
        heights = [c.height for c in self.adjacents]
        if self.height < min(heights):
            self.bassin_center = self
            self.bassin_size = self.set_bassin_center()
            return True
        return False

    def set_bassin_center(self):
        size = 0
        for cell in self.adjacents:
            if cell.height < 9 and cell.bassin_center is None:
                cell.bassin_center = self.bassin_center
                size += cell.set_bassin_center()
        return size + 1

    def __repr__(self):
        return f"({self.x},{self.y}){self.__str__()}"

    def __str__(self):
        adj = "".join([str(c.height) for c in self.adjacents])
        return f"{self.height}({adj})"


class DayInput(WebInput):
    def __init__(self, day=9, **kwargs):
        super().__init__(day=day, **kwargs)
        self.cells = dict()
        rows = self.get_content()
        for x in range(len(rows[0])):
            for y in range(len(rows)):
                self.cells[(x, y)] = Cell(x, y, int(rows[y][x]))
        for cell in self.cells.values():
            cell.set_adjacents(self.cells)

    def get_low_points(self):
        return [c for c in self.cells.values() if c.is_low_point()]

    def get_risk_sum(self):
        points = self.get_low_points()
        risk = [c.height + 1 for c in points]
        return sum(risk)

    def part_one(self):
        risk = self.get_risk_sum()
        print(f"Part one: {risk}")

    def part_two(self):
        low_points = self.get_low_points()
        points = sorted([c.bassin_size for c in low_points], reverse=True)
        total = points[0] * points[1] * points[2]
        print(f"Part two: {total}")


DayInput(test=False).part_two()
