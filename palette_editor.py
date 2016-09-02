from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from collections.abc import Sequence
from dock_window import DockWindow
from collections import OrderedDict

class Color():
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b

    def asHexString(self):
        return "%0.2X" % self.r + "%0.2X" % self.g  + "%0.2X" % self.b

class IndexedPalette(Sequence):
    def load(self, palette_file):
        with open(palette_file, "rb") as f:
            while True:
                rgb = f.read(3)
                if len(rgb) < 3:
                    return
                self.colors.append(Color(rgb[0],rgb[1],rgb[2]))

    def __init__(self, palette_file):
        self.colors = []
        self.load(palette_file)

    def __getitem__(self, index):
        return self.colors[index]

    def __len__(self):
        return len(self.colors)

class ColorRegisters():
    def __init__(self, count=5, names_list=None):
        self.registers = OrderedDict()
        if names_list is None:
            for i in range(count):
                self.registers["Color " + str(i)] = i * 16
        else:
            i=0
            for name in names_list:
                self.registers[name] = i * 16
                i += 16

class ColorFrame(QFrame):
    clicked = pyqtSignal(int, name='colorClicked')
    def __init__(self, parent, palette_index=0):
        super().__init__(parent)
        self.palette_index = palette_index

    def mousePressEvent(self, event):
        print("mousePressEvent " + str(self.palette_index))
        self.clicked.emit(self.palette_index)
        # return super().mousePressEvent(self, event)

class ColorRegisterEditor(QWidget):
    def __init__(self, parent, palette, color_registers):
        super().__init__(parent)
        gridLayout = QGridLayout()
        self.setLayout(gridLayout)
        self.palette = palette
        for y in range(16):
            for x in range(int(len(self.palette)/16)):
                frame = ColorFrame(self)
                hex_color = "#" + self.palette[y*16 + x].asHexString()
                frame.setStyleSheet(".QFrame { background-color: " + hex_color + "; border: solid 1px white; border-radius: 1px; }")
                gridLayout.addWidget(frame,y,x)


class ColorPicker(QWidget):
    color_picked = pyqtSignal(int, name='colorPicked')

    def __init__(self, parent, palette):
        super().__init__(parent)
        gridLayout = QGridLayout()
        gridLayout.setVerticalSpacing(0)
        gridLayout.setHorizontalSpacing(0)
        self.setLayout(gridLayout)
        self.palette = palette
        for i in range(len(self.palette)):
            y = int(i/16)
            x = i % 16
            colorButton = ColorFrame(self, i)
            colorButton.clicked.connect(self.color_picked)
            colorButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            hex_color = "#" + self.palette[i].asHexString()
            colorButton.setStyleSheet(".ColorFrame { background-color: " + hex_color + "; border: solid 1px white; border-radius: 1px; margin: 0px; padding: 0px; }")
            gridLayout.addWidget(colorButton,y,x)


class PaletteEditorWindow(DockWindow):
    def colorPickedHandler(self, value):
        print("Color chosen = " + str(value))


    def __init__(self, parent):
        super().__init__(parent, "Palette editor")

        mainWidget = QWidget(self)
        vLayout = QVBoxLayout(mainWidget)
        #palette = PaletteWidget(self);
        # vLayout.addWidget(palette)

        palette_file = "examples/arkanoid/laoo.act"
        palette = IndexedPalette(palette_file)

        # colorRegEdit = ColorRegisterEditor(self, palette)
        # vLayout.addWidget(colorRegEdit)

        paletteColorPicker = ColorPicker(self, palette)
        paletteColorPicker.color_picked.connect(self.colorPickedHandler)
        vLayout.addWidget(paletteColorPicker)

        button = QPushButton("button")
        vLayout.addWidget(button)
        mainWidget.setLayout(vLayout)

        self.setWidget(mainWidget)

