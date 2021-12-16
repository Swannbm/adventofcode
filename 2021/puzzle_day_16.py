from utils import WebInput


DAY = int(__file__.split(".")[0].split("_")[-1])


def hex2bin(hex_str):
    result = ""
    for c in hex_str:
        num = int(c, 16)
        b = bin(num)[2:]
        result += b.zfill(4)
    return result


def packet_factory(bin_str):
    packet = Packet(bin_str)
    if packet.type == 4:
        return PacketNumber(bin_str)
    else:
        return PacketOperator(bin_str)


class Packet:
    def __init__(self, bin):
        """Start of the binary string representing the packet
        Might contains more than what is needed"""
        self.initial_bin = bin
        self.version = self.get_version()
        self.type = self.get_type()
        self.value = None
        self.end_bin = None

    def get_version(self):
        return int(self.initial_bin[0:3], 2)

    def get_type(self):
        return int(self.initial_bin[3:6], 2)

    def get_value(self):
        raise NotImplementedError()

    def get_version_sum(self):
        raise NotImplementedError()

    def get_remaining_bin(self):
        raise NotImplementedError()


class PacketNumber(Packet):
    """Type 4 packet that contains a number"""

    def __init__(self, *args):
        super().__init__(*args)
        self.get_value()

    def get_value(self):
        i = 6
        chunk = ""
        while True:
            chunk += self.initial_bin[i + 1:i + 5]
            if self.initial_bin[i] == "0":
                break
            i += 5
        self.value = int(chunk, 2)
        self.end_bin = i + 5
        return self.value

    def get_version_sum(self):
        return self.version

    def get_remaining_bin(self):
        return self.initial_bin[self.end_bin:]


class PacketOperator(Packet):
    """Contains a fixed number of subpackets"""

    def __init__(self, *args):
        super().__init__(*args)
        # properties
        self.operator_type = self.initial_bin[6]
        self.size = None
        self.subpackets = None
        # init
        self.get_size()
        self.get_subpackets()

    def get_subpacket_start(self):
        if self.initial_bin[6] == "0":
            return 7 + 15
        else:
            return 7 + 11

    def get_size(self):
        if not self.size:
            end = self.get_subpacket_start()
            self.size = int(self.initial_bin[7:end], 2)
        return self.size

    def get_subpackets(self):
        if not self.subpackets:
            if self.operator_type == "0":
                self.subpackets = self.get_subpackets_fixed()
            else:
                self.subpackets = self.get_subpackets_count()
        return self.subpackets

    def get_subpackets_count(self):
        subpackets = []
        start = self.get_subpacket_start()
        self.remaining_bin = self.initial_bin[start:]
        i = 0
        while i < self.size:
            i += 1
            subpackets.append(packet_factory(self.remaining_bin))
            self.remaining_bin = subpackets[-1].get_remaining_bin()
        return subpackets

    def get_subpackets_fixed(self):
        subpackets = []
        start = self.get_subpacket_start()
        end = start + self.size
        remaining_bin = self.initial_bin[start: end]
        while True:
            subpackets.append(packet_factory(remaining_bin))
            remaining_bin = subpackets[-1].get_remaining_bin()
            if len(remaining_bin) <= 6:
                break
        self.remaining_bin = self.initial_bin[end:]
        return subpackets

    def get_value(self):
        values = [p.get_value() for p in self.subpackets]
        if self.type == 0:  # sum
            return sum(values)
        elif self.type == 1:  # product
            result = 1
            for v in values:
                result *= v
            return result
        elif self.type == 2:  # minimum
            return min(values)
        elif self.type == 3:  # maximum
            return max(values)
        elif self.type == 5:  # greater
            if values[0] > values[1]:
                return 1
            else:
                return 0
        elif self.type == 6:  # less
            if values[0] < values[1]:
                return 1
            else:
                return 0
        elif self.type == 7:  # equal
            if values[0] == values[1]:
                return 1
            else:
                return 0

    def get_version_sum(self):
        total = sum([p.get_version_sum() for p in self.subpackets])
        return self.version + total

    def get_remaining_bin(self):
        return self.remaining_bin


class DayInput(WebInput):
    def __init__(self, **kwargs):
        super().__init__(day=DAY, **kwargs)
        self.get_content()
        self.bin = hex2bin(self.rows[0])

    def print(self):
        print()

    def part_one(self):
        packet = packet_factory(self.bin)
        version_sum = packet.get_version_sum()
        print(f"Part one: {version_sum}")
        print(f"Part two: {packet.get_value()}")


test = False
DayInput(test=test).part_one()
# DayInput(test=test).part_two()
