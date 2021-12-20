from utils import WebInput
from termcolor import cprint
from itertools import combinations
from time import time
import os


DAY = int(__file__.split(".")[0].split("_")[-1])


class DoneExplode(BaseException):
    pass


class DoneSplit(BaseException):
    pass


cnt_print = 1


def format(number):
    global cnt_print
    print(f"{cnt_print} => ", end="")
    cnt_print += 1
    if isinstance(number, SnailNumber):
        number = str(number)
    color = ['white', 'blue', 'green', 'yellow', 'magenta', 'red']
    deep = 0
    prev = ""
    for i, c in enumerate(number):
        next = number[i+1] if i < len(number) - 1 else ""
        if c == "[":
            deep += 1
        elif c == " ":
            continue
        if c.isdigit() and (prev.isdigit() or next.isdigit()):
            cprint(c, color[deep], 'on_cyan', end="")
        else:
            cprint(c, color[deep], end="")
        if c == "]":
            deep -= 1
        prev = c
    print()


class IntChained:
    def __init__(self, value):
        if isinstance(value, IntChained):
            self.value = value.value
        else:
            self.value = value
        self.next = None
        self.prev = None

    def set_next(self, other):
        if other:
            self.next = other
            other.prev = self

    def set_prev(self, other):
        if other:
            self.prev = other
            other.next = self

    def __add__(self, other):
        return IntChained(self.value + other.value)

    def __iadd__(self, other):
        self.value = self.value + other.value
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            v = self.value - other
        else:
            v = self.value - other.value
        return IntChained(v)

    def __gt__(self, other):
        if isinstance(other, int):
            return self.value > other
        else:
            return self.value > other.value

    def __floordiv__(self, other):
        if isinstance(other, int):
            v = self.value // other
        else:
            v = self.value // other
        return IntChained(v)

    def explode(self):
        return False

    def split(self):
        return False

    def increase_deep(self):
        pass

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class SnailNumber:
    def __init__(self, data: list(), deep=0, parent=None):
        self.parent = parent
        self.deep = deep

        if isinstance(data[0], int):
            self.left = IntChained(data[0])
        elif isinstance(data[0], IntChained):
            self.left = data[0]
        elif isinstance(data[0], SnailNumber):
            self.left = data[0]
        else:
            self.left = SnailNumber(data[0], deep=deep+1, parent=self)

        if isinstance(data[1], int):
            self.right = IntChained(data[1])
        elif isinstance(data[1], IntChained):
            self.right = data[1]
        elif isinstance(data[1], SnailNumber):
            self.right = data[1]
        else:
            self.right = SnailNumber(data[1], deep=deep+1, parent=self)

    def __add__(self, other):
        other.increase_deep()
        self.increase_deep()
        end = list(self.get_nodes())[-1]
        start = list(other.get_nodes())[0]
        end.next = start
        start.prev = end
        n = SnailNumber([self, other])
        n.reduce()
        return n

    def increase_deep(self):
        self.deep += 1
        self.left.increase_deep()
        self.right.increase_deep()

    @property
    def lint(self):
        return not isinstance(self.left, SnailNumber)

    @property
    def rint(self):
        return not isinstance(self.right, SnailNumber)

    def make_list_chained(self):
        self.nodes = list(self.get_nodes())
        for i in range(len(self.nodes)):
            if i < len(self.nodes) - 1:
                self.nodes[i].next = self.nodes[i + 1]
            if i > 0:
                self.nodes[i].prev = self.nodes[i - 1]

    def get_nodes(self):
        if self.lint:
            yield self.left
        else:
            for n in self.left.get_nodes():
                yield n
        if self.rint:
            yield self.right
        else:
            for n in self.right.get_nodes():
                yield n

    def can_explode(self):
        if self.lint and self.rint:
            if self.deep >= 4:
                return True
        return False

    def explode(self):
        if self.can_explode():
            node = IntChained(0)
            node.next = self.right.next
            node.prev = self.left.prev
            if self.left.prev:
                self.left.prev += self.left
                self.left.prev.next = node
            if self.right.next:
                self.right.next += self.right
                self.right.next.prev = node
            return node
        else:
            node = self.left.explode()
            if node:
                self.left = node
                raise DoneExplode()
            node = self.right.explode()
            if node:
                self.right = node
                raise DoneExplode()

    def split(self):

        def split_node(node):
            n1 = node // 2
            n2 = node - n1
            n1.set_next(n2)
            n1.set_prev(node.prev)
            n2.set_next(node.next)
            return [n1, n2]

        if self.lint:
            if self.left > 9:
                pair = split_node(self.left)
                self.left = SnailNumber(pair, deep=self.deep+1)
                raise DoneSplit()
        else:
            self.left.split()
        if self.rint:
            if self.right > 9:
                pair = split_node(self.right)
                self.right = SnailNumber(pair, deep=self.deep+1)
                raise DoneSplit()
        else:
            self.right.split()

    def reduce(self):
        i = 0
        todo = True
        while todo:
            i += 1
            format(self)
            try:
                self.explode()
                self.split()
                todo = False
            except (DoneExplode, DoneSplit):
                todo = True

    def __str__(self):
        left = str(self.left) if self.lint else str(self.left)
        right = str(self.right) if self.rint else self.right.__str__()
        return f"[{left}, {right}]"

    def __repr__(self):
        return self.__str__()

    def get_magnitude(self):
        total = 0
        if self.lint:
            total += 3 * self.left.value
        else:
            total += 3 * self.left.get_magnitude()
        if self.rint:
            total += 2 * self.right.value
        else:
            total += 2 * self.right.get_magnitude()
        return total


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        self.get_content()

    def part_one(self):
        ans = SnailNumber(eval(self.rows[0]))
        ans.make_list_chained()
        ans.reduce()
        for row in self.rows[1:]:
            node = SnailNumber(eval(row))
            node.make_list_chained()
            ans = ans + node
            print(f"Magnitude = {ans.get_magnitude()}")

    def part_two(self):
        def make_addition(a, b):
            s1 = SnailNumber(eval(a))
            s1.make_list_chained()
            s2 = SnailNumber(eval(b))
            s2.make_list_chained()
            s3 = s1 + s2
            return s3.get_magnitude()
        m = 0
        cnt = 0
        intermediates = []
        combinates = list(combinations(self.rows, 2))
        cnt_max = len(combinates)
        for a, b in combinates:
            start_inter = time()
            cnt += 1
            m = max(
                m,
                make_addition(a, b),
                make_addition(b, a),
            )
            intermediates.append(time() - start_inter)
            os.system('clear')
            print(f"Progression: {100 * cnt/cnt_max:.0f}%")
            remaining = ((cnt_max - cnt) * sum(intermediates) / cnt)
            remaining_m = int(remaining // 60)
            remaining_s = int(remaining % 60)
            print(f"remaining : {remaining_m:>2} min et {remaining_s:>2} sec")
        print(f"Magnitude max found = {m}")

    def part_three(self):
        combinates = list(combinations(self.rows, 2))
        for a, b in combinates:
            s1 = SnailNumber(eval(a))
            s1.make_list_chained()
            s2 = SnailNumber(eval(b))
            s2.make_list_chained()
            s1 + s2
            s2 + s1


test = True
DayInput(test=test).part_three()
# DayInput(test=test).part_two()
