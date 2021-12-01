from utils import Input
from itertools import product


class Seat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.next_state = None
        self.adjacents = []

    def evaluate_next_state(self):
        self.next_state = None
        nb = [1 for _ in self.adjacents if _.occupied]
        nb = sum(nb)
        if nb == 0 and self.occupied is False:
            # seat will become occupied
            self.next_state = True
        if nb >= 4 and self.occupied is True:
            # trop de monde la personne s'en va
            self.next_state = False

    def next(self):
        if self.next_state is not None:
            self.occupied = self.next_state
        self.next_state = None

    def __str__(self):
        return "#" if self.occupied else "L"

    def __repr__(self):
        return f"({self.x},{self.y}) {self}"


class Map(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = {}
        for y, row in enumerate(self.get_content()):
            for x, c in enumerate(row):
                if c == "L":
                    self.grid[(x, y)] = Seat(x, y)
        self.max_x = x
        self.max_y = y
        for seat in self.grid.values():
            # get x,y for all adjacents
            x = seat.x
            y = seat.y
            position = list(product((x - 1, x, x + 1), (y - 1, y, y + 1)))
            # remove current cell
            position.pop(position.index((x, y)))
            for (x, y) in position:
                if (x, y) in self.grid.keys():
                    seat.adjacents.append(self.grid[(x, y)])

    def is_stabilized(self):
        moves = [1 for _ in self.grid.values() if _.next_state is not None]
        moves = sum(moves)
        if moves > 0:
            return False

    def count_seaters(self):
        seaters = [1 for _ in self.grid.values() if _.occupied]
        seaters = sum(seaters)
        return seaters

    def stabilize(self):
        # first round to initialize the system
        for seat in self.grid.values():
            seat.evaluate_next_state()
        # wait stabilization
        while self.is_stabilized() is False:
            # new state
            for seat in self.grid.values():
                seat.next()
            # evaluate next state
            for seat in self.grid.values():
                seat.evaluate_next_state()

    def print(self):
        for y in range(0, self.max_y + 1):
            for x in range(0, self.max_x + 1):
                cell = self.grid.get((x, y), None)
                print(cell if cell else ".", end="")
            print()


inputs = Map(day=11)
inputs.stabilize()
print(f"Part 1: {inputs.count_seaters()}")
