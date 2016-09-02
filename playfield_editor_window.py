from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dock_window import DockWindow

class PlayfieldEditorWindow(DockWindow):
    def __init__(self, parent):
        super().__init__(parent, "Playfield editor")
        self.something = QListWidget(self)
        self.setWidget(self.something)