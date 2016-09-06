from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ColorFrame(QFrame):
    clicked = pyqtSignal(object, name='colorClicked')
    double_clicked = pyqtSignal(object, name='colorDoubleClicked')

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

    def mouseDoubleClickEvent(self,event):
        print("Double click!")
        self.double_clicked.emit(self.key)

    def mousePressEvent(self, event):
        print("ColorFrame mousePressEvent {0}".format(str(self.key)))
        self.clicked.emit(self.key)
        # return super().mousePressEvent(self, event)

    def ColorToHexString(self, color):
            return "#" + "%0.2X" % color.red() + "%0.2X" % color.green() + "%0.2X" % color.blue()

    def setColor(self, color):
        self.color = self.ColorToHexString(color)
        self.updateStyle()

    def setBorder(self, color):
        self.borderColor = self.ColorToHexString(color)
        self.updateStyle()

    def deactivate(self):
        self.borderColor = "#000000"
        self.updateStyle()

    def activate(self):
        self.borderColor = "#FFFF00"
        self.updateStyle()
