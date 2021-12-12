from utils import WebInput
import numpy as np

WebInput.init(7)


class Crabe(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=7, **kwargs)
        self.crabes = [int(i) for i in self.get_content()[0].split(",")]

    def most_efficient_aligment(self):
        return np.median(self.crabes)

    def average(self):
        return round(np.average(self.crabes))

    def align_crabes(self):
        position = self.most_efficient_aligment()
        fuel = 0
        for crabe in self.crabes:
            fuel += sum(range(abs(crabe-position) + 1))
        return fuel

    def part_one(self):
        required_fuel = self.align_crabes()
        print(f"Part one: {required_fuel}")

    def part_two(self):
        self.most_efficient_aligment = self.average
        required_fuel = self.align_crabes()
        print(f"Part two: {required_fuel}")


# Crabe(test=False).part_one()

Crabe(test=False).part_two()
