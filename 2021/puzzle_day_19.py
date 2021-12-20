from utils import WebInput
import re
import numpy as np
from termcolor import cprint


DAY = int(__file__.split(".")[0].split("_")[-1])

RE_POSITION = re.compile(r"(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)")
RE_SCANNER = re.compile(r"--- scanner (?P<num>-?\d+) ---")

ROT = [
    np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1))),
    np.array(((1, 0, 0), (0, 0, -1), (0, 1, 0))),
    np.array(((1, 0, 0), (0, -1, 0), (0, 0, -1))),
    np.array(((1, 0, 0), (0, 0, 1), (0, -1, 0))),
    np.array(((0, -1, 0), (1, 0, 0), (0, 0, 1))),
    np.array(((0, 0, 1), (1, 0, 0), (0, 1, 0))),
    np.array(((0, 1, 0), (1, 0, 0), (0, 0, -1))),
    np.array(((0, 0, -1), (1, 0, 0), (0, -1, 0))),
    np.array(((-1, 0, 0), (0, -1, 0), (0, 0, 1))),
    np.array(((-1, 0, 0), (0, 0, -1), (0, -1, 0))),
    np.array(((-1, 0, 0), (0, 1, 0), (0, 0, -1))),
    np.array(((-1, 0, 0), (0, 0, 1), (0, 1, 0))),
    np.array(((0, 1, 0), (-1, 0, 0), (0, 0, 1))),
    np.array(((0, 0, 1), (-1, 0, 0), (0, -1, 0))),
    np.array(((0, -1, 0), (-1, 0, 0), (0, 0, -1))),
    np.array(((0, 0, -1), (-1, 0, 0), (0, 1, 0))),
    np.array(((0, 0, -1), (0, 1, 0), (1, 0, 0))),
    np.array(((0, 1, 0), (0, 0, 1), (1, 0, 0))),
    np.array(((0, 0, 1), (0, -1, 0), (1, 0, 0))),
    np.array(((0, -1, 0), (0, 0, -1), (1, 0, 0))),
    np.array(((0, 0, -1), (0, -1, 0), (-1, 0, 0))),
    np.array(((0, -1, 0), (0, 0, 1), (-1, 0, 0))),
    np.array(((0, 0, 1), (0, 1, 0), (-1, 0, 0))),
    np.array(((0, 1, 0), (0, 0, -1), (-1, 0, 0))),
]


TREE = {
    10: 0, 28: 10, 27: 10, 25: 27, 21: 27, 18: 25, 17: 18, 14: 25, 11: 25,
    5: 21, 4: 28, 3: 5, 1: 25, 29: 18, 26: 21, 22: 3, 20: 4, 19: 22,
    13: 19, 9: 13, 8: 22, 7: 1, 2: 8, 24: 8, 23: 24, 16: 13, 15: 24,
    12: 24, 6: 12,
}


def manhattan(start, other):
    return sum(abs(start[i] - other[i]) for i in range(3))


class Scanner:
    def __init__(self, numero, i=0, v=np.array((0, 0, 0)), f=None, t=None):
        self.numero = numero
        self.beacons = []
        self.rotation_index = i
        self.rotation = ROT[i]
        self.vector = np.array(v)
        self.from_scanner = f
        if not t:
            t = []
        self.to_scanners = t
        self.done_find_transfo = []

    def add_beacon(self, x, y, z):
        self.beacons.append(np.array((x, y, z)))

    def get_scanners_position(self):
        scanners = [self.vector, ]
        for other in self.to_scanners:
            scanners += [
                self.rotation.dot(v) + self.vector
                for v in other.get_scanners_position()
            ]
        return scanners

    def transform_beacons(self, rotation, vector):
        def trans(beacon):
            return rotation.dot(beacon) + vector
        return [trans(b) for b in self.beacons]
        # num_cores = multiprocessing.cpu_count()
        # func = Parallel(n_jobs=num_cores)
        # transformed_beacons = func(delayed(trans)(b) for b in self.beacons)
        # return transformed_beacons

    def get_all_beacons(self):
        for other in self.to_scanners:
            if other.from_scanner != self:
                raise Exception("Incohérence")
            other_beacons = other.get_all_beacons()
            self.add_new_beacons(other_beacons)
        if self.from_scanner:
            beacons = self.transform_beacons(self.rotation, self.vector)
        else:
            beacons = self.beacons
        return beacons

    def add_new_beacons(self, others_beacons):
        original_beacons = self.beacons.copy()
        for other in others_beacons:
            found = False
            for beacon in original_beacons:
                cond = other == beacon
                if cond[0] and cond[1] and cond[2]:
                    found = True
                    break
            if not found:
                self.beacons.append(other)

    def count_common_beacons(self, other_beacons):
        """count how many beacons are identical (coordinate the same) between
        beacons list and others list"""
        cnt = 0
        for beacon in self.beacons:
            for other in other_beacons:
                cond = other == beacon
                if cond[0] and cond[1] and cond[2]:
                    cnt += 1
                    break
        return cnt

    def find_transfo(self, other_scanner):
        """On boucle sur tous les beacons de self (A) et tous les beacons de
        other (B). Pour chaque pair (A, B), on va vérifier si finalement c'est
        le même beacon (ie. A==B). Pour cela:
        1. initialisation : i = 0
        2. Pour chaque beacon dans self (appelé A)
            3. Pour chaque beacon dans other_scanner (appelé B)
                4. on applique à B une ROT[i] (ie. la première fois (i==0)
                   c'est la rotation identique, donc B ne change pas)
                    5. on calcule le vecteur permettant de passer de A à B
                    6. on appliqe le vecteur de transformation obtenu à tous
                       les autres beacons de other
                    7. on compare les nouveaux beacons de other (après
                       transformation) au beacon de self et on compte le nombre
                       d'identique
                    8. s'il y a au moins 11 beacons identiques, on a trouver la
                       transformation de self vers other scanner on sort
                    9. sinon, et si i < 24, on incrémente i et on reprend à 4.
        Renvoi TRUE si on a trouvé un lien vers
        """
        if other_scanner in self.done_find_transfo:
            return False
        self.done_find_transfo.append(other_scanner)
        i = 0
        for beacon in self.beacons:
            for other_beacon in other_scanner.beacons:
                for i in range(24):
                    t_other_beacon = ROT[i].dot(other_beacon)
                    vector = beacon - t_other_beacon
                    other_beacons = other_scanner.transform_beacons(
                        ROT[i], vector
                    )
                    cnt_commons = self.count_common_beacons(other_beacons)
                    if cnt_commons >= 12:
                        self.to_scanners.append(other_scanner)
                        other_scanner.from_scanner = self
                        other_scanner.rotation = ROT[i]
                        other_scanner.rotation_index = i
                        other_scanner.vector = vector
                        return True
        return False

    def manhattan(self, other):
        return sum(abs(self.vector[i] - other.vector[i]) for i in range(3))

    def __gt__(self, other):
        return self.numero > other.numero

    def __eq__(self, other):
        return self.numero == other.numero

    def __repr__(self):
        return str(self.numero)

    def __str__(self):
        return str(self.numero)


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        self.get_content()
        self.scanners = []
        for row in self.rows:
            matches = RE_POSITION.match(row)
            if matches:
                self.scanners[-1].add_beacon(
                    int(matches.group("x")),
                    int(matches.group("y")),
                    int(matches.group("z")),
                )
            else:
                numero = int(RE_SCANNER.match(row).group("num"))
                self.scanners.append(Scanner(numero))

    def part_one(self):
        linked = [self.scanners[0], ]
        to_be_linked = self.scanners[1:].copy()
        while len(to_be_linked) > 0:
            found = False
            other_scanner = to_be_linked.pop()
            print(f"Try to link {other_scanner}", end="")
            for scanner in linked:
                print(".", end="")
                if scanner.find_transfo(other_scanner):
                    cprint(f"success! With {scanner}.", 'green')
                    linked.insert(0, other_scanner)
                    found = True
                    break
            if not found:
                cprint("failed...", 'red')
                to_be_linked.insert(0, other_scanner)
        beacons = self.scanners[0].get_all_beacons()
        print(f"Part one: {len(beacons)}")

    def part_two(self):
        for k, v in TREE.items():
            print(f"{k}, {v}")
            self.scanners[v].find_transfo(self.scanners[k])
        m = 0
        positions = self.scanners[0].get_scanners_position()
        for pos in positions:
            for other in positions:
                d = manhattan(pos, other)
                m = max(m, d)
        print(f"Part two: {m}")


input = DayInput(test=False)
input.part_two()
