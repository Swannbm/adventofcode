from utils import InputGrouped


class GroupAnswer:
    def __init__(self, row):
        row = row.replace(" ", "")
        self.letters = set(c for c in row)

    def count(self):
        return len(self.letters)

    def __str__(self):
        return f"{self.letters}"


input = InputGrouped(day=6)
answers = input.get_objects(GroupAnswer)
total = sum(_.count() for _ in answers)
print(f"Part 1: {total}")


class GroupAnswerEveryone(GroupAnswer):
    def __init__(self, row):
        answers = map(lambda x: set(c for c in x), row.split(" "))
        self.letters = set.intersection(*answers)


answers = input.get_objects(GroupAnswerEveryone)
total = sum(_.count() for _ in answers)
print(f"Part 2: {total}")
