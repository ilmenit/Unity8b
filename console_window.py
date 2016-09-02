from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dock_window import DockWindow

class ConsoleWindow(DockWindow):
    def append(self, text):
        if self.textEdit != None:
            self.textEdit.append(text)

    def clear(self):
        if self.textEdit != None:
            self.textEdit.clear()

    def __init__(self, parent):
        super().__init__(parent, "Console")
        self.textEdit = QTextEdit(self)
        self.textEdit.append("This is a console...")
        self.textEdit.setReadOnly(True)
        self.setWidget(self.textEdit)