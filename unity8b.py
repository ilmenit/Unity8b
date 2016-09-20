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


Inspector Window to edit properties of assets

Asset can have:
- code
= events
- slots of other assets

Code generation is different for:
- Objects with single instance (direct access to data)
- Objects in array (y,x)



'''

#!/usr/bin/env python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main_window import MainWindow
import qdarkstyle
import unity8b_rc

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def loadDarkStyle():
    f = QFile(":/styles/dark.qss")
    if not f.exists():
        return None
    f.open(QFile.ReadOnly | QFile.Text)
    ts = QTextStream(f)
    stylesheet = ts.readAll()
    return stylesheet

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
