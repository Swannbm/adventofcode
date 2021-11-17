import re
from utils import Input


CONTAINER_RE = r"(?P<container>^[\w\s]+) bags contain"
CONTENT_RE = r"(?P<content>[\d]{1,2} [\w\s]+){1,1}bags?"


class Rule:
    def __init__(self, row):
        """
        Example:
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        dotted black bags contain no other bags.
        """
        self.rules = []  # contains
        self.contents = dict()
        self.color = re.match(CONTAINER_RE, row)["container"]
        for content in [m["content"] for m in re.finditer(CONTENT_RE, row)]:
            nb = content.split()[0]
            name = content[len(nb):].strip()
            self.contents[name] = int(nb)

    def __str__(self):
        content = [f"{v} {k}" for k, v in self.contents.items()]
        return f"{self.color} <= {', '.join(content)}"

    def __repr__(self):
        return self.__str__()

    def can_contains(self, color):
        return color in self.contents.keys()

    def get_bags(self, start=1):
        total = start
        for rule in self.rules:
            nb = rule.get_bags()
            total += nb * self.contents[rule.color]
        return total


input = Input(day=7)
rules = list(input.iter(Rule))

to_search = ["shiny gold"]
searched = []
containers = []

while len(to_search) > 0:
    needle = to_search.pop()
    for rule in rules:
        if rule.color != needle:
            if rule.can_contains(needle):
                if rule.color not in to_search + searched:
                    to_search.append(rule.color)
                    containers.append(rule)
    searched.append(needle)

print(f"Part 1: {len(containers)}")


def get_rule(color):
    for rule in rules:
        if rule.color == color:
            return rule


# création des liens entre les règles
for rule in rules:
    rule.rules = [get_rule(color) for color in rule.contents.keys()]

nb = get_rule("shiny gold").get_bags(start=0)
print(f"Part 2: {nb}")
