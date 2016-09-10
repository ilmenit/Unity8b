'''
Good examples:
- pixelator and scribble - as an FONT and GFX editor
- editable tree model - object hierarchy
- simple tree model -

Naming convention in the projecT:
- Palette - set of color registers
- Playfield - screen memory where you put tiles
- Tiles -
- Tileset - set of fonts
'''

#!/usr/bin/env python
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main_window import MainWindow
import unity8b_rc

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':

    # add exception hendling
    import sys
    sys.excepthook = except_hook

    app = QApplication(sys.argv)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
