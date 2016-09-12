from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from custom_widgets import *
from indexed_palette import *
from asset import *
from copy import copy

class PaletteEditorWindow(AssetEditorWindow):
    color_register_picked = pyqtSignal(object, name='colorRegisterPicked')
    inform_color_picker = pyqtSignal(object, name='informColorPicker')

    def colorRegisterPickedHandler(self):
        print("colorRegisterPickedHandler")
        register = self.sender().key
        self.activateColorRegister(register)
        self.inform_color_picker.emit(self.asset.data[self.selected_color])

    def activateColorRegister(self, register):
        print("Activating : " + str(register))
        if register not in self.frames:
            return
        if self.selected_color is not None:
            self.frames[self.selected_color].deactivate()
        self.selected_color = register
        self.frames[self.selected_color].activate()

    def changeColorRegister(self, register, value):
        print("changeColorRegister " + str(register) + " to " + str(value))
        old_state = self.asset.getState()
        new_state = copy(old_state)
        new_state[register] = value
        self.undoStack.push(CommandChangeAsset(self.asset, old_state, new_state))

    def changeSelectedColorRegister(self, value):
        self.changeColorRegister(self.selected_color, value)

    def ColorDoubleClicked(self):
        self.parent().colorPickerWindow.show()

    def createWidget(self):
        self.mainWidget = QWidget(self)

        verticalLayout = QVBoxLayout()
        self.paletteNameLabel = QLabel(self.asset.name)
        verticalLayout.addWidget(self.paletteNameLabel)
        gridLayout = QGridLayout()
        verticalLayout.addLayout(gridLayout)

        gridLayout.setVerticalSpacing(0)
        gridLayout.setHorizontalSpacing(0)

        for i in range(len(self.asset.data)):
            value = self.asset.data[i]
            #print(str(i) + " value " + str(value))
            y = int(i / 16)
            x = i % 16
            colorButton = ColorFrame(self, i)
            self.frames[i] = colorButton
            color = global_indexed_palette[value]
            colorButton.setColor(color)
            colorButton.clicked.connect(self.color_register_picked)
            colorButton.clicked.connect(self.colorRegisterPickedHandler)
            colorButton.double_clicked.connect(self.ColorDoubleClicked)
            colorButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            gridLayout.addWidget(colorButton, y, x)

        self.mainWidget.setLayout(verticalLayout)
        self.setWidget(self.mainWidget)
        self.activateColorRegister(0)

    def setAsset(self, asset):
        self.asset = asset
        self.asset.data.dataChanged.connect(self.dataChangedHandler)
        self.createWidget()

    def dataChangedHandler(self):
        #print("PALETTE DATA CHANGED")
        for i in range(len(self.asset.data)):
            value = self.asset.data[i]
            self.frames[i].setColor(global_indexed_palette[value])

    def windowName(self):
        return "Palette"

    def __init__(self, parent):
        super().__init__(parent)
        self.asset = None
        self.selected_color = None
        self.frames = dict()
