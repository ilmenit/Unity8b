from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
from custom_widgets import *
from indexed_palette import *

class ColorRegisterEditor(QWidget):
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


class PaletteEditorWindow(DockWindow):
    def colorRegisterPickedHandler(self, value):
        print("Color register chosen = " + str(value))
        self.paletteColorPicker.activateColor(self.color_registers[value])

    def colorPickedHandler(self, value):
        print("Color chosen = " + str(value))
        self.colorRegEdit.changeSelectedColorRegister(value)

    def __init__(self, parent):
        super().__init__(parent, "Palette")

        palette_file = "examples/arkanoid/laoo.act"
        palette = IndexedPalette(palette_file)
        self.color_registers = ColorRegisters()
        self.mainWidget = ColorRegisterEditor(self, palette, self.color_registers)
        self.setWidget(self.mainWidget)

