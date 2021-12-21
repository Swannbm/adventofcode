from utils import WebInput



DAY = int(__file__.split(".")[0].split("_")[-1])


class Player:
    def __init__(self, position):
        self.position = position
        self.score = 0

    def play(self, value):
        self.position += value
        while self.position > 10:
            self.position -= 10
        self.score += self.position


class Dice:
    def __init__(self):
        self.values = list(range(1, 101))
        self.cnt = 0

    def roll(self):
        res = self.values[self.cnt % 100]
        self.cnt += 1
        return res

    def last_rolls(self, nb):
        i = self.cnt % 100
        if i - nb >= 0:
            return self.values[i - nb: i]
        else:
            return self.values[100 - nb + i:100] + self.values[0:i]

    def rolls(self, nb=3):
        return sum(self.roll() for i in range(nb))


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        if self.test:
            self.players = [Player(4), Player(8)]
        else:
            self.players = [Player(7), Player(2)]
        self.dice = Dice()

    def loop(self):
        i = 0
        while max([p.score for p in self.players]) < 1000:
            d = self.dice.rolls(nb=3)
            self.players[i % 2].play(d)
            if self.test:
                self.print(i)
            i += 1
        return self.dice.cnt * min(p.score for p in self.players)

    def print(self, i):
        d = self.dice.last_rolls(nb=3)
        msg = (
            f"Player {i % 2 + 1} rolls {d} and moves to space "
            f"{self.players[i % 2].position} for a total score of "
            f"{self.players[i % 2].score}."
        )
        print(msg)

    def part_one(self):
        total = self.loop()
        print(f"Part one: {total}")

    def part_two(self):
        total = 0
        print(f"Part two: {total}")


# test = False
# DayInput(test=test).part_one()
# DayInput(test=test).part_two()


from functools import cache


def fix_pos(pos):
    while pos > 10:
        pos -= 10
    return pos



@cache
def get_wins(p1_pos, p1_score, p2_pos, p2_score, p_to_play):
    p1_wins = p2_wins = 0
    if p_to_play == 1:
        for r1 in range(1, 4):
            for r2 in range(1, 4):
                for r3 in range (1, 4):
                    new_p1_pos = fix_pos(p1_pos + r1 + r2 + r3)
                    new_p1_score = p1_score + new_p1_pos
                    if new_p1_score >= 21:
                        p1_wins += 1
                    else:
                        w1, w2 = get_wins(
                            new_p1_pos, new_p1_score, p2_pos, p2_score, 2
                        )
                        p1_wins += w1
                        p2_wins += w2
    else:
        for r1 in range(1, 4):
            for r2 in range(1, 4):
                for r3 in range (1, 4):
                    new_p2_pos = fix_pos(p2_pos + r1 + r2 + r3)
                    new_p2_score = p2_score + new_p2_pos
                    if new_p2_score >= 21:
                        p2_wins += 1
                    else:
                        w1, w2 = get_wins(
                            p1_pos, p1_score, new_p2_pos, new_p2_score, 1
                        )
                        p1_wins += w1
                        p2_wins += w2
    return p1_wins, p2_wins


w1, w2 = get_wins(7, 0, 2, 0, 1)
print(f"ans={max(w1, w2)}")
