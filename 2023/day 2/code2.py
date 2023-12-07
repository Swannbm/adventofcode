from pathlib import Path
import re


def pgreen(text, **kwargs):
    print(f"\033[92m{text}\033[0m", **kwargs)


def pred(text, **kwargs):
    print(f"\033[91m{text}\033[0m", **kwargs)


input_a = open(Path(__file__).parent / "input_a.txt", "r").read()

total = 0

for i, game in enumerate(input_a.split("\n")):
    game = game.replace(f"Game {i+1}:", "")
    print(f"Game {i+1}:", end=" ")
    red = []
    blue = []
    green = []
    for draw in game.split(";"):
        print(draw, end=" ")
        for colored in draw.split(","):
            nb = int(re.search(r"\d+", colored).group(0))
            # game possible with 12 red cubes, 13 green cubes, and 14 blue
            if "blue" in colored:
                blue.append(nb)
            elif "green" in colored:
                green.append(nb)
            elif "red" in colored:
                red.append(nb)
    print(
        "max red:",
        max(red),
        "max green:",
        max(green),
        "max blue:",
        max(blue),
        end=" ",
    )
    power = max(red) * max(green) * max(blue)
    print(f"({power})")
    total += power
print(f"total: {total}")
