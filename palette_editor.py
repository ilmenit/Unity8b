from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from collections.abc import Sequence
from dock_window import DockWindow
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


class ColorFrame(QFrame):
    clicked = pyqtSignal(object, name='colorClicked')

    def updateStyle(self):
        #print("updateStyle")
        style = '.ColorFrame { background-color: ' + self.color + "; border: 1px solid " + self.borderColor + "; border-radius: 0px; }"
        self.setStyleSheet(style)

    def __init__(self, parent, key=0):
        super().__init__(parent)
        self.key = key
        self.color = '#ff00ff'
        self.borderColor = '#000000'
        self.updateStyle()

    def mousePressEvent(self, event):
        print("ColorFrame mousePressEvent {0}".format(str(self.key)))
        self.clicked.emit(self.key)
        # return super().mousePressEvent(self, event)

    def setColor(self, color):
        self.color = "#" + color.asHexString()
        self.updateStyle()

    def setBorder(self, color):
        self.borderColor = "#" + color.asHexString()
        self.updateStyle()

    def deactivate(self):
        self.borderColor = "#000000"
        self.updateStyle()

    def activate(self):
        self.borderColor = "#FFFF00"
        self.updateStyle()


class ColorRegisterEditor(QWidget):
    '''
    Currently this implementation is very similar to ColorPicker but I assume later it can be different e.g.
    for sprite color editing where third color is combination of two
    '''
    color_register_picked = pyqtSignal(object, name='colorRegisterPicked')

    def colorRegisterPickedHandler(self):
        sender = self.sender()
        self.activatecolorRegister(sender.key)

    def activatecolorRegister(self, register):
        print("Activating : " + str(register))
        if register not in self.frames:
            return
        if self.selectedRegister is not None:
            self.frames[self.selectedRegister].deactivate()
        self.selectedRegister = register
        self.frames[self.selectedRegister].activate()

    def changeSelectedColorRegister(self, value):
        if self.selectedRegister is None:
            return
        self.color_registers[self.selectedRegister] = value
        self.frames[self.selectedRegister].setColor(self.palette[value])

    def __init__(self, parent, palette, color_registers):
        super().__init__(parent)
        gridLayout = QGridLayout(self)
        self.frames = dict()
        self.selectedRegister = None
        self.setLayout(gridLayout)
        gridLayout.setVerticalSpacing(0)
        gridLayout.setHorizontalSpacing(0)
        self.palette = palette
        self.color_registers = color_registers
        i = 0
        for key, value in self.color_registers.items():
            print(str(i) + " Key " + key)
            y = int(i / 16)
            x = i % 16
            # colorRegisterButton = ColorFrame(self, i)
            # color = self.palette[value]
            colorButton = ColorFrame(self, key)
            self.frames[key] = colorButton
            color = self.palette[value]
            colorButton.setColor(color)
            colorButton.clicked.connect(self.color_register_picked)
            colorButton.clicked.connect(self.colorRegisterPickedHandler)
            colorButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            gridLayout.addWidget(colorButton, y, x)
            if i==0:
                self.activatecolorRegister(key)
            i += 1


class ColorPicker(QWidget):
    color_picked = pyqtSignal(object, name='colorPicked')

    def activateColor(self, color_index):
        if color_index not in self.frames:
            return
        if self.selectedColor is not None:
            self.frames[self.selectedColor].deactivate()
        self.selectedColor = color_index
        self.frames[self.selectedColor].activate()

    def colorPickedHandler(self):
        sender = self.sender()
        self.activateColor(sender.key)

    def __init__(self, parent, palette):
        super().__init__(parent)
        gridLayout = QGridLayout(self)
        self.frames = dict()
        self.selectedColor = None
        self.setLayout(gridLayout)
        gridLayout.setVerticalSpacing(0)
        gridLayout.setHorizontalSpacing(0)
        self.palette = palette
        for color_index in range(len(self.palette)):
            y = int(color_index / 16)
            x = color_index % 16
            colorButton = ColorFrame(self, color_index)
            self.frames[color_index] = colorButton
            color = self.palette[color_index]
            colorButton.setColor(color)
            colorButton.clicked.connect(self.color_picked)
            colorButton.clicked.connect(self.colorPickedHandler)
            colorButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            gridLayout.addWidget(colorButton, y, x)


class PaletteEditorWindow(DockWindow):
    def colorRegisterPickedHandler(self, value):
        print("Color register chosen = " + str(value))
        self.paletteColorPicker.activateColor(self.color_registers[value])

    def colorPickedHandler(self, value):
        print("Color chosen = " + str(value))
        self.colorRegEdit.changeSelectedColorRegister(value)

    def __init__(self, parent):
        super().__init__(parent, "Palette editor")

        mainWidget = QWidget(self)
        vLayout = QVBoxLayout(mainWidget)

        palette_file = "examples/arkanoid/laoo.act"
        palette = IndexedPalette(palette_file)

        self.color_registers = ColorRegisters()
        self.colorRegEdit = ColorRegisterEditor(self, palette, self.color_registers)
        self.colorRegEdit.color_register_picked.connect(self.colorRegisterPickedHandler)
        vLayout.addWidget(self.colorRegEdit)
        vLayout.setStretchFactor(self.colorRegEdit, 20)

        self.paletteColorPicker = ColorPicker(self, palette)
        self.paletteColorPicker.color_picked.connect(self.colorPickedHandler)
        vLayout.addWidget(self.paletteColorPicker)
        vLayout.setStretchFactor(self.paletteColorPicker, 80)

        mainWidget.setLayout(vLayout)

        self.setWidget(mainWidget)
