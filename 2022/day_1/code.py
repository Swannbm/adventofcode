from pathlib import Path


class Input:
    def __init__(self, puzzle, day=1, year=2022):
        self.day = day
        self.year = year
        self.puzzle = puzzle

    def get_filename(self):
        if self.puzzle == "test":
            return "inputs_exemple.txt"
        elif self.puzzle == "a":
            return "inputs_a.txt"
        else:
            return "inputs_b.txt"

    def path(self):
        return Path(__file__).parent / self.get_filename()

    def keep_line(self, row):
        if row == "":
            return False
        return True

    def get_raw_content(self):
        with open(self.path(), "r") as file:
            self.content = file.read()
        return self.content

    def get_content(self):
        content = self.get_raw_content().split("\n")
        self.rows = [_ for _ in content if self.keep_line(_)]
        return self.rows

    def get_int(self):
        return list(map(int, self.get_content()))

    def iter(self, klass):
        for row in self.get_content():
            yield klass(row)


class Puzzle(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elves = list()

    def get_content(self):
        content = self.get_raw_content().split("\n")
        self.elves.append([])
        for row in content:
            if row != "":
                self.elves[-1].append(row)
            else:
                self.elves.append([])
        return self.elves

    def sort(self):
        return sorted([sum(map(int, e)) for e in self.get_content()])

    def solve(self):
        print(f"{self.puzzle}={self.sort()[-1]}")


class PuzzleB(Puzzle):
    def solve(self):
        print(f"b={sum(self.sort()[-3:])}")


Puzzle("test").solve()
Puzzle("a").solve()
PuzzleB("a").solve()
