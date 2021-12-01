from pathlib import Path


class Input:
    def __init__(self, day=1, **kwargs):
        self.day = day

    def get_filename(self):
        return f"day_{self.day}.txt"

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
