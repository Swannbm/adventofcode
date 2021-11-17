from utils import Input


class Map(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = self.get_content()

    def has_tree(self, index_line, index_col):
        row = self.rows[index_line]
        index_col = index_col % len(row)
        c = "O"
        if row[index_col].upper() == "#":
            c = "X"
        self.rows[index_line] = f"{row[:index_col]}{c}{row[index_col+1:]}"
        return True if c == "X" else False

    def is_arrived(self, index_line):
        if index_line >= len(self.rows):
            return True
        return False

    def cpt_trees(self, right, down):
        current_col = current_line = cpt_tree = 0
        while self.is_arrived(current_line) is False:
            if self.has_tree(current_line, current_col):
                cpt_tree += 1
            current_line += down
            current_col += right
        return cpt_tree


map = Map(day=3)


print(f"Part 1: {map.cpt_trees(3, 1)}")


print("part 2:")
total = 1
for right, down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    cpt = Map(day=3).cpt_trees(right, down)
    total *= cpt
    print(f"({right}, {down}) {cpt}")

print(total)
