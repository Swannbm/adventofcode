from pathlib import Path
import requests


class Input:
    def __init__(self, day=1, year=2021, test=False):
        self.day = day
        self.year = year
        self.test = test

    def get_filename(self):
        if not self.test:
            return f"day_{self.day}.txt"
        else:
            return f"day_{self.day}_test.txt"

    def path(self):
        path = Path(__file__).parent
        return path / "inputs" / self.get_filename()

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


class InputGrouped(Input):
    def keep_line(self, row):
        return True

    def get_objects(self, klass):
        items = []
        input = []
        for row in self.get_content():
            if row == "":
                items.append(klass(" ".join(input)))
                input = []
            else:
                input.append(row)
        return items


class WebInput(Input):
    def get_cookie_value(self):
        path = Path(__file__).parent.parent
        cookiepath = path / ".cookie_value"
        with open(cookiepath, "r") as file:
            return file.readline().strip()

    def get_remote_input(self):
        content = ""
        if not self.test:
            url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"
            cookies = {'session': self.get_cookie_value()}  # noqa: E501
            content = requests.get(url, cookies=cookies).text
        with open(self.path(), "w") as f:
            f.write(content)

    def get_content(self, force_download=False):
        if not self.path().exists() or force_download:
            self.get_remote_input()
        rows = super().get_content()
        if len(rows) == 1 and rows[0].startswith("Please don't repeatedly"):
            self.get_remote_input()
            return super().get_content()
        return rows

    @classmethod
    def init(self, day):
        WebInput(day=day, test=True).get_content()
        WebInput(day=day).get_content(force_download=True)


class Cell:
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.value = value
        self.adjacents = []

    def set_adjacents(self, cells, diag=False):
        adjacents = [
            (-1, 0),  # gauche
            (1, 0),  # droite
            (0, -1),  # haut
            (0, 1),  # bas
        ]
        if diag:
            adjacents += [
                (-1, -1),  # gauche / haut
                (-1, 1),  # gauche / bas
                (1, -1),  # droite / haut
                (1, 1),  # droite / bas
            ]
        for i, j in adjacents:
            pos = (self.x + i, self.y + j)
            if pos in cells.keys():
                self.adjacents.append(cells[pos])

    def __repr__(self):
        return f"({self.x},{self.y}){self.__str__()}"

    def __str__(self):
        adj = "".join([str(c.value) for c in self.adjacents])
        return f"{self.value}({adj})"
