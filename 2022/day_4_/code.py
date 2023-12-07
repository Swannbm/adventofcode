from pathlib import Path
from random import choice


content = open(Path(__file__).parent / "input_a.txt", "r").read()
content = [_ for _ in content.split("\n") if _]


def convert(line):
    r1, r2 = [_.split("-") for _ in line.split(",")]
    return list(map(int, r1)), list(map(int, r2))


count = 0
count_b = 0
for line in content:
    r1, r2 = convert(line)
    if (r1[0] <= r2[0] and r1[1] >= r2[1]) or (r1[0] >= r2[0] and r1[1] <= r2[1]):
        count += 1

    if (r1[0] <= r2[0] <= r1[1]) or (r1[0] <= r2[1] <= r1[1]) or (r2[0] <= r1[0] <= r2[1]) or (r2[0] <= r1[1] <= r2[1]):
        count_b += 1

print(count)
print(count_b)
