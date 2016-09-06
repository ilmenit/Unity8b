from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dock_window import DockWindow

class SceneWindow(DockWindow):
    def __init__(self, parent):
        super().__init__("Scene View", parent)
        self.playfields = QListWidget(self)
        self.playfields.addItems((
            "Score Playfield",
            "Main Playfield",
            "Stats Playfield"
        ))
        self.setWidget(self.playfields)