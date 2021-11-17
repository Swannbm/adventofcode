from utils import Input


class InputSeat(Input):
    def get_seats(self):
        """FBFBBFFRLR"""
        for row in self.get_content():
            line = (0, 127)
            col = (0, 7)
            for c in row:
                move_line = int((line[1] - line[0]) / 2) + 1
                move_col = int((col[1] - col[0]) / 2) + 1
                if c == "F":
                    line = (line[0], line[1] - move_line)
                elif c == "B":
                    line = (line[0] + move_line, line[1])
                elif c == "R":
                    col = (col[0] + move_col, col[1])
                elif c == "L":
                    col = (col[0], col[1] - move_col)
                else:
                    raise Exception("Unknow move")
            if line[0] != line[1] or col[0] != col[1]:
                raise Exception("Seat not found")
            yield line[0] * 8 + col[0]


input = InputSeat(day=5)
ids = [seat for seat in input.get_seats()]
print(f"Part 1: {max(ids)}")

availables = [line * 8 + col for line in range(11, 112) for col in range(0, 8)]

for id in ids:
    availables.pop(availables.index(id))


print(availables)
