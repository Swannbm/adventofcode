import re

tree = """Try to link 10.success! With 0.
Try to link 28.success! With 10.
Try to link 27..success! With 10.
Try to link 25.success! With 27.
Try to link 21..success! With 27.
Try to link 18..success! With 25.
Try to link 17.success! With 18.
Try to link 14....success! With 25.
Try to link 11.....success! With 25.
Try to link 5.....success! With 21.
Try to link 4.........success! With 28.
Try to link 3..success! With 5.
Try to link 1.........success! With 25.
Try to link 29........success! With 18.
Try to link 26..........success! With 21.
Try to link 22....success! With 3.
Try to link 20......success! With 4.
Try to link 19..success! With 22.
Try to link 13.success! With 19.
Try to link 9.success! With 13.
Try to link 8.....success! With 22.
Try to link 7.........success! With 1.
Try to link 2..success! With 8.
Try to link 24...success! With 8.
Try to link 23.success! With 24.
Try to link 16.......success! With 13.
Try to link 15...success! With 24.
Try to link 12....success! With 24.
Try to link 6.success! With 12."""

R = re.compile(r"Try to link (?P<from>[\d]+)\.+success! With (?P<to>[\d]+)\.")
print("tree = {")
for line in tree.split("\n"):
    matches = R.match(line)
    scanner = matches.group("from")
    other_scanner = matches.group("to")
    print(f"{scanner}: {other_scanner}, ", end="")
print("}")


