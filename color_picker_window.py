from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
from custom_widgets import *
from indexed_palette import *
from asset_playfield_palette import *

class ColorPickerWindow(DockWindow):
    color_picked = pyqtSignal(object, name='colorPicked')

    def activateColor(self, color_index):
        #print("ColorPickerWindow::activateColor " + str(color_index))
        if color_index not in self.frames:
            return
        if self.selectedColor is not None:
            self.frames[self.selectedColor].deactivate()
        self.selectedColor = color_index
        self.frames[self.selectedColor].activate()

    def colorPickedHandler(self):
        #print("colorPickedHandler")
        sender = self.sender()
        self.activateColor(sender.key)

    def createWidget(self):
        self.mainWidget = QWidget(self)
        gridLayout = QGridLayout(self)
        self.mainWidget.setLayout(gridLayout)
        gridLayout.setVerticalSpacing(0)
        gridLayout.setHorizontalSpacing(0)
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
        self.setWidget(self.mainWidget)

    def __init__(self, parent):
        super().__init__("Color picker", parent)
        palette_file = "palettes/laoo.act"
        self.palette = IndexedPalette(palette_file)
        self.frames = dict()
        self.selectedColor = None
        self.createWidget()

