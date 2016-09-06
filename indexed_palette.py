from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from collections.abc import Sequence
from collections import OrderedDict

class IndexedPalette(Sequence):
    def load(self, palette_file):
        with open(palette_file, "rb") as f:
            while True:
                rgb = f.read(3)
                if len(rgb) < 3:
                    return
                self.colors.append(QColor(rgb[0], rgb[1], rgb[2]))

    def __init__(self, palette_file):
        self.colors = []
        self.load(palette_file)

    def __getitem__(self, index):
        return self.colors[index]

    def __len__(self):
        return len(self.colors)


class PlayfieldPalette(list):
    def __init__(self, count=5):
        super().__init__()
        for i in range(count):
            self.append(i * 16 + 5)
