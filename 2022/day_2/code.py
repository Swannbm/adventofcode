# rock = A - X - 1
# scosspr = C - Z - 3
# paper = B - Y - 2
from pathlib import Path

points = {"X": 1, "Y": 2, "Z": 3}


content = open(Path(__file__).parent / "input_a.txt", "r").read()
# content = open(Path(__file__).parent / "input_test.txt", "r").read()
score = 0
for round in content.split("\n"):
    try:
        o, m = round.split(" ")
        score += points[m]
        if (o == "A" and m == "X") or (o == "B" and m == "Y") or (o == "C" and m == "Z"):
            score += 3
        if (o == "A" and m == "Y") or (o == "B" and m == "Z") or (o == "C" and m == "X"):
            score += 6
    except ValueError:
        pass

print("First=", score)


transco = {
    "X": {"A": "Z", "B": "X", "C": "Y"},
    "Y": {"A": "X", "B": "Y", "C": "Z"},
    "Z": {"A": "Y", "B": "Z", "C": "X"},
}
# X = loose
# y = draw
# z = win
content = open(Path(__file__).parent / "input_a.txt", "r").read()
score = 0
for round in content.split("\n"):
    try:
        o, state = round.split(" ")
        m = transco[state][o]
        score += points[m]
        if (o == "A" and m == "X") or (o == "B" and m == "Y") or (o == "C" and m == "Z"):
            score += 3
        elif (o == "A" and m == "Y") or (o == "B" and m == "Z") or (o == "C" and m == "X"):
            score += 6
    except ValueError:
        pass
print("second=", score)