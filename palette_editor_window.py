from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
from custom_widgets import *
from indexed_palette import *

class CommandChangeColorRegisterValue(QUndoCommand):
    def __init__(self, palette_editor_window, register, value):
        super(CommandChangeColorRegisterValue, self).__init__("ChangeColorRegisterValue " + str(register) + "=" + str(value))
        self.palette_editor_window = palette_editor_window
        self.register = register
        self.value = value
        self.old_value = self.palette_editor_window.color_registers[self.register]

    def changeColor(self, register, value):
        print("CommandChangeColor")
        self.palette_editor_window.color_registers[register] = value
        self.palette_editor_window.frames[register].setColor(self.palette_editor_window.palette[value])
        self.palette_editor_window.palette_changed.emit()

    def redo(self):
        print("CommandChangeColorRegisterValue::REDO")
        self.changeColor(self.register, self.value)

    def undo(self):
        print("CommandChangeColorRegisterValue::UNDO")
        self.changeColor(self.register, self.old_value)

class PaletteEditorWindow(DockWindow):
    color_register_picked = pyqtSignal(object, name='colorRegisterPicked')
    inform_color_picker = pyqtSignal(object, name='informColorPicker')
    palette_changed = pyqtSignal(name='paletteChanged')

    def focusInEvent(self, event):
        self.parent().activateUndoStack(self.undoStack)

    def colorRegisterPickedHandler(self):
        print("colorRegisterPickedHandler")
        sender = self.sender()
        self.activateColorRegister(sender.key)
        self.inform_color_picker.emit(self.color_registers[self.selectedRegister])

    def activateColorRegister(self, register):
        print("Activating : " + str(register))
        if register not in self.frames:
            return
        if self.selectedRegister is not None:
            self.frames[self.selectedRegister].deactivate()
        self.selectedRegister = register
        self.frames[self.selectedRegister].activate()

    def changeColorRegister(self, register, value):
        print("changeColorRegister")
        self.undoStack.push(CommandChangeColorRegisterValue(self, register, value))

    def changeSelectedColorRegister(self, value):
        self.changeColorRegister(self.selectedRegister, value)

    def createWidget(self):
        self.mainWidget = QWidget(self)

        verticalLayout = QVBoxLayout()
        self.paletteNameLabel = QLabel("<< Palette name here >>")
        verticalLayout.addWidget(self.paletteNameLabel)
        gridLayout = QGridLayout()
        verticalLayout.addLayout(gridLayout)

        gridLayout.setVerticalSpacing(0)
        gridLayout.setHorizontalSpacing(0)
        i = 0
        for key, value in self.color_registers.items():
            print(str(i) + " Key " + key)
            y = int(i / 16)
            x = i % 16
            colorButton = ColorFrame(self, key)
            self.frames[key] = colorButton
            color = self.palette[value]
            colorButton.setColor(color)
            colorButton.clicked.connect(self.color_register_picked)
            colorButton.clicked.connect(self.colorRegisterPickedHandler)
            colorButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            gridLayout.addWidget(colorButton, y, x)
            if i==0:
                self.activateColorRegister(key)
            i += 1

        self.mainWidget.setLayout(verticalLayout)
        self.setWidget(self.mainWidget)

    def setPalette(self, palette):
        pass


    def __init__(self, parent):
        super().__init__("Palette", parent)
        palette_file = "examples/arkanoid/laoo.act"
        self.palette = IndexedPalette(palette_file)
        self.color_registers = ColorRegisters()
        self.selectedRegister = None
        self.frames = dict()
        self.createWidget()
