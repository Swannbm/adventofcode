from pathlib import Path
import string

print(ord("a") - 96)
print(ord("A") - 64 + 26)

VALUES = {
    letter: ord(letter) - 96 for letter in string.ascii_lowercase
}
VALUES.update(
    {
        letter: ord(letter) - 64 + 26 for letter in string.ascii_uppercase
    }
)


content = open(Path(__file__).parent / "input_a.txt", "r").read()
content = [_ for _ in content.split("\n") if _]

score = 0
for line in content:
    items = list(line)
    i = int(len(items) / 2)
    common_items = {item for item in items[:i] if item in items[i:]}
    for item in common_items:
        score += VALUES[item]

print("partie 1:", score)

score = 0
for i in range(2, len(content), 3):
    common = {item for item in content[i] if item in content[i-1] and item in content[i-2]}
    score += sum([VALUES[item] for item in common])

print("partie 2:", score)
