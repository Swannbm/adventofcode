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

    def get_content(self):
        with open(self.path(), "r") as file:
            content = file.read().split("\n")
        return [_ for _ in content if self.keep_line(_)]

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
        return super().get_content()
