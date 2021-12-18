from utils import WebInput


DAY = int(__file__.split(".")[0].split("_")[-1])


class SnailNumber:
    def __init__(self, data: list(), deep=0, parent=None):
        self.parent = parent
        self.deep = deep
        if isinstance(data[0], int):
            self.left = data[0]
            self.lint = True
        else:
            self.left = SnailNumber(data[0], deep=deep+1, parent=self)
            self.lint = False
        if isinstance(data[1], int):
            self.right = data[1]
            self.rint = True
        else:
            self.right = SnailNumber(data[1], deep=deep+1, parent=self)
            self.rint = False

    def pair(self):
        return [self.left, self.right]

    def add_left_up(self, value):
        if self.lint:
            self.left += value
        elif self.parent:
            self.parent.add_left_up(value)
        elif not self.rint:
            self.right.add_self_down(value)

    def add_left_down(self, value):
        if self.lint:
            self.left += value
        else:
            self.left.add_left_down(value)

    def add_right_up(self, value):
        if self.rint:
            self.right += value
        elif self.parent:
            self.parent.add_right_up(value)
        elif not self.lint:
            self.left.add_left_down(value)

    def add_right_down(self, value):
        if self.rint:
            self.right += value
        else:
            self.right.add_right_down(value)

    def can_explode(self):
        if self.lint and self.rint:
            if self.deep >= 4:
                return True
        return False

    def explode(self):
        if not self.lint:
            if self.left.can_explode():
                self.parent.add_left_up(self.left.left)
                self.add_right_up(self.left.right)
                self.left = 0
            else:
                self.left.explode()
        if not self.rint:
            if self.right.can_explode():
                self.parent.add_right_up(self.right.right)
                self.add_left_up(self.right.left)
                self.right = 0
            else:
                self.right.explode()

    def add_pair(self, pair):
        if pair is None:
            return None
        if self.lint:
            self.left += pair[0]
            pair[0] = 0
        if self.rint:
            self.right += pair[1]
            pair[1] = 0
        if pair[0] != 0 or pair[1] != 0:
            return pair
        else:
            return None

    def reduce(self):
        top_order = dict()
        if not self.lint:
            order = self.left.reduce()
            top_order.update(self.apply_order(order))
            if top_order:
                return top_order

    def apply_order(self, order):
        if 'add_left' in order.keys() and self.lint:
            self.left += order.pop('add_left')
        if 'add_right' in order.keys() and self.rint:
            self.right += order.pop('add_right')
        return order

    def split(self):
        if self.lint and self.left > 9:
            pair = [self.left // 2, self.left - self.left // 2]
            self.left = SnailNumber(pair, deep=self.deep+1)
        if self.rint and self.right > 9:
            pair = [self.right // 2, self.right - self.right // 2]
            self.right = SnailNumber(pair, deep=self.deep+1)

    def __str__(self):
        left = str(self.left) if self.lint else self.left.__str__()
        right = str(self.right) if self.rint else self.right.__str__()
        return f"[{left}, {right}]"

    def __repr__(self):
        return self.__str__()


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        for row in self.get_content():
            node = SnailNumber(eval(row))
            node.explode()
            print(node)

    def print(self):
        print()

    def part_one(self):
        total = 0
        print(f"Part one: {total}")

    def part_two(self):
        total = 0
        print(f"Part two: {total}")


test = True
DayInput(test=test).part_one()
# DayInput(test=test).part_two()
