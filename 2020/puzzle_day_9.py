from itertools import product
from utils import Input


class ValidInput(Input):
    def __init__(self, tail=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []
        self.tail = tail

    def is_valid(self, value):
        if len(self.data) < self.tail:
            return True
        tail_data = self.data[-self.tail:]
        for a, b in product(tail_data, tail_data):
            if a + b == value:
                return True
        return False

    def get_first_invalid(self):
        self.data = []
        for value in self.get_int():
            if not self.is_valid(value):
                return value
            else:
                self.data.append(value)
        return None

    def add_min_max(self, value):
        for i in range(1, len(self.data) + 1):
            if sum(self.data[-i:]) == value:
                return min(self.data[-i:]) + max(self.data[-i:])
        return None

    def get_contiguous(self, first_invalid):
        self.data = []
        for value in self.get_int():
            self.data.append(value)
            val_min_max = self.add_min_max(first_invalid)
            if val_min_max:
                return val_min_max


input = ValidInput(day=9, tail=25)
first = input.get_first_invalid()
print(f"Part 1: {first}")

print(f"Part 2: {input.get_contiguous(first)}")
