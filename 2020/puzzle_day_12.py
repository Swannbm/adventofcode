from utils_copy import WebInput


class Ship:
    def __init__(self):
        self.direction_degree = 0
        self.direction = "E"
        self.x = self.y = 0

    def manhattan(self):
        return abs(self.x) + abs(self.y)

    def process_order(self, order, distance):
        if order == "N":
            self.y += distance
        elif order == "S":
            self.y -= distance
        elif order == "E":
            self.x += distance
        elif order == "W":
            self.x -= distance
        elif order == "F":
            self.process_order(self.direction, distance)
        elif order == "R":
            self.set_direction(distance, clockwise=True)
        elif order == "L":
            self.set_direction(distance, clockwise=False)

    def set_direction(self, degree, clockwise=True):
        if clockwise:
            self.direction_degree += degree
        else:
            self.direction_degree -= degree
        while self.direction_degree < 0:
            self.direction_degree += 360
        while self.direction_degree >= 360:
            self.direction_degree -= 360

        if self.direction_degree == 0:
            self.direction = "E"
        elif self.direction_degree == 90:
            self.direction = "S"
        elif self.direction_degree == 180:
            self.direction = "W"
        elif self.direction_degree == 270:
            self.direction = "N"


class Ship2(Ship):
    def __init__(self):
        super().__init__()
        self.waypoint_x = 10
        self.waypoint_y = 1

    def process_order(self, order, distance):
        if order == "N":
            self.waypoint_y += distance
        elif order == "S":
            self.waypoint_y -= distance
        elif order == "E":
            self.waypoint_x += distance
        elif order == "W":
            self.waypoint_x -= distance
        elif order == "F":
            self.move_ship(distance)
        elif order == "R":
            self.set_direction(distance, clockwise=True)
        elif order == "L":
            self.set_direction(distance, clockwise=False)

    def set_direction(self, degree, clockwise=True):
        if clockwise:
            degree *= -1

        if degree == 90 or degree == -270:
            self.waypoint_y, self.waypoint_x = self.waypoint_x, -self.waypoint_y
        elif degree == 180 or degree == -180:
            self.waypoint_y, self.waypoint_x = -self.waypoint_y, -self.waypoint_x
        elif degree == 270 or degree == -90:
            self.waypoint_y, self.waypoint_x = -self.waypoint_x, self.waypoint_y

    def move_ship(self, cnt):
        self.x += cnt * self.waypoint_x
        self.y += cnt * self.waypoint_y

    def print(self):
        print(f"position=({self.x}, {self.y})")
        print(f"waypoint=({self.waypoint_x}, {self.waypoint_y})")
        print()


input = WebInput(day=12, year=2020, test=False)
ship = Ship()
ship2 = Ship2()
for row in input.get_content():
    order = row[:1]
    distance = int(row[1:])
    ship.process_order(order, distance)
    ship2.process_order(order, distance)
    ship2.print()

print(f"Distance part 1 = {ship.manhattan()}")
print(f"Distance part 2 = {ship2.manhattan()}")
