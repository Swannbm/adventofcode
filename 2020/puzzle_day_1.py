
from pathlib import Path

path = Path(__file__).parent
print(path)

filepath = path / "inputs" / "day_1.txt"

with open(filepath, "r") as file:
    content = file.read().split("\n")[:-1]

numbers = list(map(int, content))
cpt = len(numbers)

for i in range(0, cpt):
    for j in range(i + 1, cpt):
        total = numbers[i] + numbers[j]
        if total == 2020:
            print(f"Found part 1: {numbers[i] * numbers[j]}")
        for k in range(j + 1, cpt):
            total = numbers[i] + numbers[j] + numbers[k]
            if total == 2020:
                print(f"Found part 2: {numbers[i] * numbers[j] * numbers[k]}")
