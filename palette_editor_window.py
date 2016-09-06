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
        self.old_value = self.palette_editor_window.playfield_palette[self.register]

    def changeColor(self, register, value):
        print("CommandChangeColor")
        self.palette_editor_window.playfield_palette[register] = value
        self.palette_editor_window.frames[register].setColor(self.palette_editor_window.full_palette[value])
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
        self.inform_color_picker.emit(self.playfield_palette[self.selectedRegister])

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

    def ColorDoubleClicked(self):
        print("DDDDDDD")
        self.parent().colorPickerWindow.show()

    def createWidget(self):
        self.mainWidget = QWidget(self)

        verticalLayout = QVBoxLayout()
        self.paletteNameLabel = QLabel("<< Palette name here >>")
        verticalLayout.addWidget(self.paletteNameLabel)
        gridLayout = QGridLayout()
        verticalLayout.addLayout(gridLayout)

        gridLayout.setVerticalSpacing(0)
        gridLayout.setHorizontalSpacing(0)

        for i in range(len(self.playfield_palette)):
            value = self.playfield_palette[i]
            print(str(i) + " value " + str(value))
            y = int(i / 16)
            x = i % 16
            colorButton = ColorFrame(self, i)
            self.frames[i] = colorButton
            color = self.full_palette[value]
            colorButton.setColor(color)
            colorButton.clicked.connect(self.color_register_picked)
            colorButton.clicked.connect(self.colorRegisterPickedHandler)
            colorButton.double_clicked.connect(self.ColorDoubleClicked)
            colorButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            gridLayout.addWidget(colorButton, y, x)
            if i==0:
                self.activateColorRegister(i)

        self.mainWidget.setLayout(verticalLayout)
        self.setWidget(self.mainWidget)

    def setPalette(self, palette):
        pass


    def __init__(self, parent):
        super().__init__("Palette", parent)
        palette_file = "examples/arkanoid/laoo.act"
        self.full_palette = IndexedPalette(palette_file)
        self.playfield_palette = PlayfieldPalette()
        self.selectedRegister = None
        self.frames = dict()
        self.createWidget()
