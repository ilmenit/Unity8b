from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import collections
pos = collections.namedtuple("pos", ("row, column"))

class DockWindow(QDockWidget):
    def __init__(self, parent, name):
        super().__init__(name)
        self.setObjectName(name)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        parent.addDockWidget(Qt.TopDockWidgetArea, self)
        parent.viewMenu.addAction(self.toggleViewAction())
