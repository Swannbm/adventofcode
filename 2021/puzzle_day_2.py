from utils import Input


class Submarine(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = 0
        self.y = 0
        self.aim = 0

    def get_final_position(self):
        rows = self.get_content()
        for row in rows:
            direction, size = row.split()
            size = int(size)
            if direction == "forward":
                self.x += size
            elif direction == "up":
                self.y -= size
            elif direction == "down":
                self.y += size
        return (self.x, self.y)

    def get_final_position_2(self):
        self.x = self.y = self.aim = 0
        rows = self.get_content()
        for row in rows:
            direction, size = row.split()
            size = int(size)
            if direction == "forward":
                self.x += size
                self.y += self.aim * size
            elif direction == "up":
                self.aim -= size
            elif direction == "down":
                self.aim += size
        return (self.x, self.y)


input = Submarine(day=2)
x, y = input.get_final_position()
print(f"Part one: {x * y}")

x, y = input.get_final_position_2()
print(f"Part two: {x * y}")
