from utils import WebInput


class LanterFish(WebInput):
    def __init__(self, loop=18, **kwargs):
        self.todo_loop = loop
        super().__init__(**kwargs)
        self.lanterns = {i: 0 for i in range(10)}
        for lantern in [int(i) for i in self.get_content()[0].split(",")]:
            self.lanterns[lantern] += 1

    def loop(self):
        self.lanterns[9] = self.lanterns[0]
        self.lanterns[7] += self.lanterns[0]
        self.lanterns[0] = 0
        for i in range(1, 10):
            self.lanterns[i - 1] = self.lanterns[i]
        self.lanterns[9] = 0

    def part_one(self):
        for i in range(self.todo_loop):
            self.loop()
            total = sum(self.lanterns.values())
            if self.test:
                print(f"After {i} day(s): {total}")
        print(f"Part: {total}")


LanterFish(day=6, test=False, loop=256).part_one()
