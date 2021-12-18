from utils import WebInput


DAY = int(__file__.split(".")[0].split("_")[-1])


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        # v = lambda x: (-1 + (1+8*x)**0.5)/2
        if self.test:
            self.target = [(20, -10), (30, -5)]
            self.vx_max = 30
            self.vy_max = 10
        else:
            self.target = [(240, -90), (292, -57)]
            self.vx_max = 292
            self.vy_max = 90

    def fire(self, vx, vy):
        px = py = 0
        while True:
            # move
            px += vx
            py += vy
            # check if we are in target
            course = self.is_in_target(px, py)
            if course == "WIN":
                return True
            if course == "MISSED":
                raise Exception("Missed target")
            if vx > 0:
                vx -= 1
            vy -= 1

    def is_in_target(self, px, py):
        cond1 = self.target[0][0] <= px <= self.target[1][0]
        cond2 = self.target[0][1] <= py <= self.target[1][1]
        if cond1 and cond2:
            return "WIN"
        cond1 = px <= self.target[1][0]
        cond2 = py >= self.target[0][1]
        if cond1 and cond2:
            return "POSSIBLE"
        return "MISSED"

    def find_correct_fire(self):
        corrects = []
        for vx in range(0, self.vx_max + 1):
            for vy in range(self.vy_max * -1, self.vy_max):
                try:
                    self.fire(vx, vy)
                    corrects.append((vx, vy))
                except:  # noqa: E722
                    pass
        return corrects

    def print(self):
        print()

    def part_one(self):
        total = 0
        print(f"Part one: {total}")

    def part_two(self):
        corrects = self.find_correct_fire()
        total = len(corrects)
        self.fire(22, 89)
        print(f"Part two: {total}")


test = False
# DayInput(test=test).part_one()
DayInput(test=test).part_two()
