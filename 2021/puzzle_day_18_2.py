from utils import WebInput


test = True
for row in WebInput(day=18, test=test).get_content():
    print(row)


def explode(row):
    cnt_brackets = 0
    for c in row:
        if c == "[":
            cnt_brackets += 1
        elif c == "]":
        elif c.is
            
