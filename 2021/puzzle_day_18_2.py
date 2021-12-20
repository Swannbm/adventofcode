from utils import WebInput


DAY = int(__file__.split(".")[0].split("_")[-1])


class Node:
    def __init__(self, value, deep):
        self.value = value
        self.deep = deep

    def __str__(self):
        return f"{self.value}({self.deep})"

    def __repr__(self):
        return self.__str__()

    def split(self):
        self.deep += 1
        n2 = Node(self.value - self.value // 2, self.deep)
        self.value = self.value // 2
        return n2

    def reset(self):
        self.value = 0
        self.deep -= 1


class Chain:
    def __init__(self, row):
        self.chain = []
        deep = 0
        for c in row:
            if c == "[":
                deep += 1
            elif c == "]":
                deep -= 1
            elif c.isdigit():
                self.chain.append(Node(int(c), deep))

    def reduce(self):
        more_loop = True
        while more_loop:
            more_loop = self.explode()
            if not more_loop:
                more_loop = self.split()

    def explode(self):
        for i, n in enumerate(self.chain):
            if n.deep == 5:
                if i > 0:
                    self.chain[i-1].value += self.chain[i].value
                if i < len(self.chain) - 2:
                    self.chain[i+2].value += self.chain[i+1].value
                self.chain[i+1].reset()
                del self.chain[i]
                return True
        return False

    def split(self):
        for i, n in enumerate(self.chain):
            if n.value > 9:
                self.chain.insert(i+1, n.split())
                return True
        return False

    def magnitude(self):
        for i in range(len(self.chain) - 1):
            if self.chain[i].deep == self.chain[i + 1]:
                pass
        # return n1 + n2
        return None

    def add(self, other_chain):
        self.chain.extend(other_chain.chain)
        for n in self.chain:
            n.deep += 1
        self.reduce()

    def format(self):
        s = ""
        cnt_brackets = 0
        for n in self.chain:
            if n.deep > cnt_brackets:
                diff = n.deep - cnt_brackets
                cnt_brackets = n.deep
                s += "[" * diff
            s += str(n.value)
            if n.deep < cnt_brackets:
                diff = cnt_brackets - n.deep
                cnt_brackets = n.deep
                s += "]" * diff
            s += ","
        s += "]" * cnt_brackets
        return s

    def __str__(self):
        return ", ".join(str(n) for n in self.chain)

    def __repr__(self):
        return self.__str__()


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        self.chains = []
        for row in self.get_content():
            self.chains.append(Chain(row))

    def add(self):
        result = self.chains[0]
        print(result.format())
        for i in range(1, len(self.chains)):
            result.add(self.chains[i])
        print(result.format())
        return result

    def print(self):
        print()

    def part_one(self):
        total = self.add()
        print(f"Part one: {total.magnitude()}")

    def part_two(self):
        total = 0
        print(f"Part two: {total}")


test = True
DayInput(test=test).part_one()
# DayInput(test=test).part_two()
