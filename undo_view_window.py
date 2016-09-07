from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dock_window import DockWindow

class UndoViewWindow(DockWindow):
    def __init__(self, parent):
        super().__init__("Undo View", parent)
        self.undoView = QUndoView(self)
        self.undoView.setStack(parent.undoStack)
        self.setWidget(self.undoView)