from collections.abc import Sequence
from collections import OrderedDict

class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def asHexString(self):
        return "%0.2X" % self.r + "%0.2X" % self.g + "%0.2X" % self.b


class IndexedPalette(Sequence):
    def load(self, palette_file):
        with open(palette_file, "rb") as f:
            while True:
                rgb = f.read(3)
                if len(rgb) < 3:
                    return
                self.colors.append(Color(rgb[0], rgb[1], rgb[2]))

    def __init__(self, palette_file):
        self.colors = []
        self.load(palette_file)

    def __getitem__(self, index):
        return self.colors[index]

    def __len__(self):
        return len(self.colors)


class ColorRegisters(OrderedDict):
    def __init__(self, count=5, names_list=None):
        super().__init__()
        if names_list is None:
            for i in range(count):
                self.__setitem__("Color " + str(i), i * 16 + 5)
        else:
            i = 0
            for name in names_list:
                self.__setitem__("Color " + str(i), i * 16 + 5)
                i += 16
