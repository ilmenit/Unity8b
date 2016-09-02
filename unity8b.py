'''
Good examples:
- pixelator and scribble - as an FONT and GFX editor
- editable tree model - object hierarchy
- simple tree model -
'''

#!/usr/bin/env python
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main_window import MainWindow

import unity8b_rc

class Game():
    name = "game_name"
    game_data = {
        "playfields": [],
        "palettes": [],
        "sounds": [],
        "sprites": [],
        "playfield_data": [],
    }
    def load(self):
        pass

    def save(self):
        pass

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
