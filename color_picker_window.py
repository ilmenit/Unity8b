from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
from custom_widgets import *
from indexed_palette import *

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

class ColorPickerWindow(DockWindow):
    def colorRegisterPickedHandler(self, value):
        print("Color register chosen = " + str(value))
        self.paletteColorPicker.activateColor(self.color_registers[value])

    def colorPickedHandler(self, value):
        print("Color chosen = " + str(value))
        self.colorRegEdit.changeSelectedColorRegister(value)

    def __init__(self, parent):
        super().__init__(parent, "Color picker")
        palette_file = "examples/arkanoid/laoo.act"
        palette = IndexedPalette(palette_file)
        self.color_registers = ColorRegisters()

        self.mainWidget = ColorPicker(self, palette)
        self.setWidget(self.mainWidget)

