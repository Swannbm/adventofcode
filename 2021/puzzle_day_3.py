from utils import WebInput


class PowerReport(WebInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count_bits = []
        self.count_lines = 0
        self.gamma = ""
        self.epsilon = ""

    def get_gamma(self, rows):
        rows = rows.copy()
        cpt_lines = len(rows) / 2
        count_bits = [int(bit) for bit in rows.pop(0)]
        for row in rows:
            bits = [int(bit) for bit in row]
            count_bits = [a + b for a, b in zip(count_bits, bits)]
        binnary = "".join(["1" if t >= cpt_lines else "0" for t in count_bits])
        return binnary

    def get_binnary(self):
        self.rows = self.get_content()
        self.count_lines = len(self.rows)
        self.count_bits = [int(bit) for bit in self.rows.pop(0)]
        for row in self.rows:
            bits = [int(bit) for bit in row]
            self.count_bits = [a + b for a, b in zip(self.count_bits, bits)]
        binnary = ''
        for total in self.count_bits:
            if total > self.count_lines / 2:
                binnary += "1"
            else:
                binnary += "0"
        return binnary

    def get_revert(self, binnary):
        revert = ""
        for c in binnary:
            revert += "0" if c == "1" else "1"
        return revert

    def get_part_1(self):
        self.gamma = self.get_gamma(self.get_content(force_download=True))
        self.epsilon = self.get_revert(self.gamma)
        return int(self.gamma, 2) * int(self.epsilon, 2)

    def get_oxygen(self):
        rows = self.get_content()
        gamma = self.get_gamma(rows)
        needle = ""
        for i in range(0, len(self.gamma)):
            needle += gamma[i]
            rows = [b for b in rows if b.startswith(needle)]
            if len(rows) == 1:
                return rows.pop()
            gamma = self.get_gamma(rows)

    def get_co2(self):
        rows = self.get_content()
        gamma = self.get_gamma(rows)
        epsilon = self.get_revert(gamma)
        needle = ""
        for i in range(0, len(self.gamma)):
            needle += epsilon[i]
            rows = [b for b in rows if b.startswith(needle)]
            if len(rows) == 1:
                return rows.pop()
            gamma = self.get_gamma(rows)
            epsilon = self.get_revert(gamma)


input = PowerReport(day=3)
b = input.get_part_1()
print(f"Part one: {b}")

oxy = input.get_oxygen()
co2 = input.get_co2()
print(f"Part two: {oxy}, {co2}")
print(f"Part two: {int(oxy, 2) * int(co2, 2)}")
