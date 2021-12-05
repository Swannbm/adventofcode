import numpy as np
from pandas import DataFrame
from utils import WebInput


class Bingo(WebInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = self.get_content()
        self.to_draw = [int(i) for i in self.rows.pop(0).split(",")]
        self.drawn = []
        self.boards = self.create_boards(self.rows.copy())

    def keep_line(self, row):
        return True

    def create_boards(self, rows):
        boards = []
        if rows[0] == "":
            del rows[0]
        df = DataFrame()
        cpt = 0
        for row in rows:
            if row.strip() != "":
                df[cpt] = [int(i) for i in row.split()]
                cpt += 1
            else:
                boards.append(df)
                df = DataFrame()
                cpt = 0
        return boards

    def draw(self):
        self.drawn.append(self.to_draw.pop(0))
        return self.drawn[-1]

    def update_boards(self, number):
        for i in range(len(self.boards)):
            self.boards[i] = self.boards[i].replace(number, np.nan)

    def is_winner(self, board):
        for col in board.count():
            if col == 0:
                return True
        for row in board.count(axis=1):
            if row == 0:
                return True
        else:
            return False

    def find_winner(self):
        for board in self.boards:
            if self.is_winner(board):
                return board
        return None

    def find_winner_part_tow(self):
        for i in range(len(self.boards)-1, -1, -1):
            if self.is_winner(self.boards[i]):
                if len(self.boards) == 1:
                    return self.boards[0]
                else:
                    del self.boards[i]
        return None

    def play_once(self):
        number = self.draw()
        self.update_boards(number)
        winner = self.find_winner()
        if self.test:
            print(number)
            i = 1 if len(self.boards) >= 2 else 0
            print(self.boards[i])
            print()
        if winner is not None:
            return number, winner
        else:
            return None, None

    def play(self):
        number, winner = self.play_once()
        while winner is None:
            number, winner = self.play_once()
        return number, winner

    def part_one(self):
        number, winner = self.play()
        result = number * winner.sum().sum()
        if self.test:
            print(f"Part one (test): {result}")
        else:
            print(f"Part one: {result}")

    def part_two(self):
        self.find_winner = self.find_winner_part_tow
        number, winner = self.play()
        result = number * winner.sum().sum()
        if self.test:
            print(f"Part two (test): {result}")
        else:
            print(f"Part two: {result}")


# Bingo(day=4, test=True).part_one()
# Bingo(day=4).part_one()
# Bingo(day=4, test=True).part_two()
Bingo(day=4).part_two()
