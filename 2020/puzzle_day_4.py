import re
from utils import Input


KEYS = [
    "byr",  # (Birth Year)
    "iyr",  # (Issue Year)
    "eyr",  # (Expiration Year)
    "hgt",  # (Height)
    "hcl",  # (Hair Color)
    "ecl",  # (Eye Color)
    "pid",  # (Passport ID)
    "cid",  # (Country ID)
]


class Passport:
    def __init__(self, input):
        """
        input example:
        hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760 byr:1931 hgt:179cm cid:35
        """
        self.data = {k: None for k in KEYS}
        for item in input.split():
            key, value = item.split(":")
            self.data[key] = value

    def is_valid(self, ignore_cid=True):
        keys = KEYS.copy()

        # faut-il ignorer le country code (cid) ?
        if ignore_cid:
            keys.pop(keys.index("cid"))

        # si une clé est manquante, le passport est invalide
        for key in keys:
            if self.data[key] is None:
                return False
        # toutes les clés sont renseignées, passport valide
        return True


class InputPassport(Input):
    def keep_line(self, row):
        return True

    def get_passports(self, klass):
        passports = []
        input = []
        for row in self.get_content():
            if row == "":
                passports.append(klass(" ".join(input)))
                input = []
            else:
                input.append(row)
        return passports


input = InputPassport(day=4)
passports = input.get_passports(Passport)
valids = [_ for _ in passports if _.is_valid()]
print(f"Part 1: {len(valids)}")


"""
VALIDATION RULES FOR PART 2:


"""

FOUR_DIGITS = re.compile(r"^[\w]{4,4}$")
HTML_COLOR = re.compile(r"^#[0-9abcdef]{6,6}$")
NINE_DIGITS = re.compile(r"^[\w]{9,9}$")


class PassportStrict(Passport):
    def clean_4_digits(self, value, min, max):
        if FOUR_DIGITS.match(value):
            if min <= int(value) <= max:
                return True
        return False

    def clean_byr(self):
        """four digits; at least 1920 and at most 2002"""
        return self.clean_4_digits(self.data["byr"], 1920, 2002)

    def clean_iyr(self):
        """iyr (Issue Year) - four digits; at least 2010 and at most 2020."""
        return self.clean_4_digits(self.data["iyr"], 2010, 2020)

    def clean_eyr(self):
        """(Expiration Year) - four digits; at least 2020 and at most 2030."""
        return self.clean_4_digits(self.data["eyr"], 2020, 2030)

    def clean_hgt(self):
        """(Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76."""
        size = self.data["hgt"][:-2]
        type = self.data["hgt"][-2:]
        if size.isdigit():
            size = int(size)
            if type == "cm":
                return 150 <= size <= 193
            elif type == "in":  # should be in(che)
                return 59 <= size <= 76
        return False

    def clean_hcl(self):
        """(Hair Color) - a # followed by exactly six characters 0-9 or a-f."""
        if HTML_COLOR.match(self.data["hcl"]):
            return True
        else:
            return False

    def clean_ecl(self):
        """(Eye Color) - exactly one of: amb blu brn gry grn hzl oth."""
        return self.data["ecl"] in "amb blu brn gry grn hzl oth".split()

    def clean_pid(self):
        """(Passport ID) - a nine-digit number, including leading zeroes."""
        return True if NINE_DIGITS.match(self.data["pid"]) else False

    def clean_cid(self):
        """(Country ID) - ignored, missing or not."""
        return True

    def is_valid(self, ignore_cid=True):
        if not super().is_valid(ignore_cid=ignore_cid):
            return False
        for key in KEYS:
            func = getattr(self, f"clean_{key}")
            if func() is False:
                return False
        return True


passports = input.get_passports(PassportStrict)
valids = [_ for _ in passports if _.is_valid()]
print(f"Part 2: {len(valids)}")
