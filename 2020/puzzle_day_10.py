from utils import Input


class Node:
    """
    a--b--d--g--h    bdgh
     \     \-f--c    bdfc
      \--d--c--
       \  \--g--
        \--c--b
    """
    def __init__(self, current_value, other_items):
        """Set a new Node with current_value and find which child nodes can
        be created from here"""
        # value of the Node
        self.value = current_value
        # children nodes
        self.nodes = []
        # Create children nodes
        for index, next_value in self.get_possible_next_nodes(other_items):
            # copy the list
            remaining_items = other_items[::]
            # remove the one we will use for the next node
            del remaining_items[:index + 1]
            self.nodes.append(Node(next_value, remaining_items))

    def get_possible_next_nodes(self, other_items):
        """Select in other_items all items that match the rule to choose next
        node. Could be overrided"""
        for i, item in enumerate(other_items[:3]):
            if abs(self.value - item) <= 3:
                yield i, item

    def filter_chains(self, chains):
        """Choose which chains will be sent to parent node."""
        selected = None
        max_value = None
        for chain in chains:
            if selected is None or max_value < chain[-1]:
                selected = chain
                max_value = chain[-1]
        return selected

    def get_chain(self):
        if not self.nodes:
            chains = [[self.value]]
        else:
            chains = [[self.value] + node.get_chain() for node in self.nodes]
        chains = self.filter(chains)
        return chains

    def count_leaf(self):
        if not self.nodes:
            if self.value >= 19:
                return 1
            else:
                return 0
        else:
            return sum(_.count_leaf() for _ in self.nodes)

    def __repr__(self):
        return f"{self.value}"


outlets = sorted(Input(day=10).get_int())
selected = [0, outlets[0]]
diffs = {
    1: 0,
    2: 0,
    3: 1,
}
diffs[outlets[0]] += 1
for i in range(1, len(outlets)):
    diff = outlets[i] - outlets[i-1]
    if diff <= 3:
        diffs[diff] += 1
        selected.append(outlets[i])
    else:
        break
selected.append(selected[-1] + 3)
print(f"Part 1: {diffs[1] * diffs[3]}")


cnt = [0] * len(selected)
cnt[-1] = 1


def get(i, j):
    if j < len(selected):
        if selected[j] - selected[i] <= 3:
            return cnt[j]
    return 0


for i in range(len(selected)-2, -1, -1):
    cnt[i] = cnt[i+1]
    cnt[i] += get(i, i+2)  # est-ce que je récupère i+2 ?
    cnt[i] += get(i, i+3)  # est-ce que je récupère i+3 ?

print(f"Part 2: {cnt[0]}")
