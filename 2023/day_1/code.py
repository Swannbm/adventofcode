from pathlib import Path


input_a = open(Path(__file__).parent / "input_a.txt", "r").read()
mapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_digit(val):
    for k, v in mapping.items():
        if val.startswith(k):
            return v


total = 0
for line in input_a.split("\n"):
    print(f"{line}=", end="")

    numbers = []
    for i, c in enumerate(line):
        if c.isdigit():
            numbers.append(c)
        else:
            val = get_digit(line[i:])
            if val:
                numbers.append(val)
    number = int(f"{numbers[0]}{numbers[-1]}")
    print(number)
    total += number

print(f"Total={total}")
