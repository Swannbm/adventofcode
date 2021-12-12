from utils import WebInput, Cell


class DayCell(Cell):
    def loop(self):
        self.value += 1

    def flash(self, from_adjacent=False):
        """
        1. Vérifie que la cellule peut flasher ou non (value != None et >= 9)
        2. Si flash:
            . ajoute 1 au compteur des flashs
            . met la valeur à None pour ne pas flasher de nouveau
            . déclenche le flash des voisins et ajoute le count des flash
            . retourne le count des flashs
        """
        if self.value is None:
            # ne peut plus flasher ce tour
            return 0
        count_flash = 0
        if from_adjacent:
            self.value += 1
        if self.value > 9:
            # la cellule va flasher
            self.value = None
            count_flash += 1
            for c in self.adjacents:
                count_flash += c.flash(from_adjacent=True)
        return count_flash

    def after_loop_hook(self):
        if self.value is None:
            self.value = 0
            return 1
        return 0


class DayInput(WebInput):
    def __init__(self, day=11, **kwargs):
        super().__init__(day=day, **kwargs)
        self.cells = dict()
        self.rows = self.get_content()
        for x in range(len(self.rows[0])):
            for y in range(len(self.rows)):
                self.cells[(x, y)] = DayCell(x, y, int(self.rows[y][x]))
        for cell in self.cells.values():
            cell.set_adjacents(self.cells, diag=True)

    def loop(self):
        for c in self.cells.values():
            c.loop()
        count_flash = 0
        for c in self.cells.values():
            count_flash += c.flash()
        for c in self.cells.values():
            c.after_loop_hook()
        if self.test:
            self.print()
        return count_flash

    def print(self):
        for y in range(len(self.rows)):
            for x in range(len(self.rows[0])):
                print(self.cells[(x, y)].value, end="")
            print()
        print()

    def part_one(self):
        count_flash = 0
        self.print()
        for i in range(100):
            count_flash += self.loop()
        print(f"Part one: {count_flash}")

    def part_two(self):
        i = 1
        while self.loop() < len(self.cells):
            i += 1
        print(f"Part two: {i}")


DayInput(test=False).part_two()
