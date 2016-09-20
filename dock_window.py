from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#import collections
#pos = collections.namedtuple("pos", ("row, column"))

class DockWindow(QDockWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.setParent(parent)
        self.setObjectName(name)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setFocusPolicy(Qt.StrongFocus)
        self.undoStack = parent.undoStack
        parent.addDockWidget(Qt.TopDockWidgetArea, self)
        parent.windowsMenu.addAction(self.toggleViewAction())
