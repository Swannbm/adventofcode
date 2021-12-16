from utils import WebInput, Cell
from queue import PriorityQueue


DAY = int(__file__.split(".")[0].split("_")[-1])


class ACell(Cell):
    def __init__(self, *args, **kwargs):
        self.goal = kwargs.pop("goal", None)
        super().__init__(*args, **kwargs)
        self.came_from = None
        self.cost_so_far = self.value
        self.goal = None
        self.goal_distance = None

    def get_priority(self):
        return self.cost_so_far + self.get_goal_distance()

    def get_goal_distance(self):
        if not self.goal_distance:
            self.goal_distance = abs(self.x - self.goal.x)
            self.goal_distance += abs(self.y - self.goal.y)
        return self.goal_distance

    def set_cost(self, from_cell):
        # coût du chemin jusque là
        new_cost = from_cell.cost_so_far
        # coût de parcours de cette cellule
        new_cost += self.value
        # coût de distance au goal
        if not self.came_from or new_cost < self.cost_so_far:
            self.came_from = from_cell
            self.cost_so_far = new_cost
            return self.get_priority()
        else:
            return None

    def __repr__(self):
        return super().__repr__() + str(self.get_priority())

    def __gt__(self, other):
        return self.get_priority() > other.get_priority()

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        self.cells = dict()
        self.frontier = PriorityQueue()
        self.get_content()

    def init_cells(self):
        for y, row in enumerate(self.rows):
            for x, val in enumerate(row):
                self.cells[(x, y)] = ACell(x, y, value=int(val))
        self.start = self.cells[(0, 0)]
        self.goal = self.cells[(x, y)]
        for cell in self.cells.values():
            cell.goal = self.goal
            cell.set_adjacents(self.cells, diag=False)

    def init_cells_2(self):
        vector_x = len(self.rows[0])
        vector_y = len(self.rows)
        for j in range(5):
            for y, row in enumerate(self.rows):
                for i in range(5):
                    ry = y + vector_y * j
                    for x, val in enumerate(row):
                        val = (int(val) - 1 + i + j) % 9 + 1
                        # print(val, end="")
                        rx = x + vector_x * i
                        self.cells[(rx, ry)] = ACell(rx, ry, value=val)
                # print("*")
        self.start = self.cells[(0, 0)]
        self.goal = self.cells[(rx, ry)]
        for cell in self.cells.values():
            cell.goal = self.goal
            cell.set_adjacents(self.cells, diag=False)

    def find_path(self):
        self.frontier.put(self.start, 0)
        while not self.frontier.empty():
            current_cell = self.frontier.get()
            if current_cell == self.goal:
                return self.get_path(current_cell)
            for adjacent_cell in current_cell.adjacents:
                priority = adjacent_cell.set_cost(current_cell)
                if priority:
                    self.frontier.put(adjacent_cell, priority)
        raise Exception("No path to goal")

    def get_path(self, cell):
        path = []
        while cell != self.start:
            path.insert(0, cell)
            cell = cell.came_from
        return path

    def print(self):
        print()

    def part_one(self):
        self.init_cells()
        path = self.find_path()
        total = sum([c.value for c in path])
        print(f"Part one: {total}")

    def part_two(self):
        self.init_cells_2()
        path = self.find_path()
        total = sum([c.value for c in path])
        print(f"Part two: {total}")


test = False
# DayInput(test=test).part_one()
DayInput(test=test).part_two()
