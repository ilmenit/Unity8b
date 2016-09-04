from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
