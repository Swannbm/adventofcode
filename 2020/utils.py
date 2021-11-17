from pathlib import Path


class Input:
    def __init__(self, day=1, **kwargs):
        self.day = day

    def get_filename(self):
        return f"day_{self.day}.txt"

    def path(self):
        path = Path(__file__).parent
        return path / "inputs" / self.get_filename()

    def get_content(self):
        with open(self.path(), "r") as file:
            content = file.read().split("\n")
        return [_ for _ in content if _ != ""]

    def get_int(self):
        return list(map(int, self.get_content()))

    def iter(self, klass):
        for row in self.get_content():
            yield klass(row)
