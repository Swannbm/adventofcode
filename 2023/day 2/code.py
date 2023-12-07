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
    print(f"Game {i+1}:", end="")
    possible = True
    for draw in game.split(";"):
        for colored in draw.split(","):
            nb = int(re.search(r'\d+', colored).group(0))
            # game possible with 12 red cubes, 13 green cubes, and 14 blue
            if "blue" in colored and nb > 14:
                possible = False
                pred(colored, end=" ")
            elif "green" in colored and nb > 13:
                possible = False
                pred(colored, end=" ")
            elif "red" in colored and nb > 12:
                possible = False
                pred(colored, end=" ")
            else:
                pgreen(colored, end=" ")
    if possible:
        total += i+1
        pgreen("===> ok")
    else:
        pred("===> ko")
print(f"total: {total}")
