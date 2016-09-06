from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from gfx_abc import *

class MemoryBuffer(Sequence, QObject):
    '''
    This class provides a view on memory buffer. It may contain multiple sub-buffers that get notified when main one is changing?

    should it be as bytearray or memoryview?
    http://www.dotnetperls.com/bytes-python

    data could be a passed one (memoryview) or local one (bytearray) - two different classes?
    '''
    data_changed = pyqtSignal(object, name='colorPicked')

    def clearChanged(self):
        self.changed = False

    def NotifyObservers(self):
        self.clearChanged()
        self.data_changed.emit(self)

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data)
        self.address = address
        self.changed = False

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.changed = True
        self.data[index] = value

    def __len__(self):
        return len(self.data)


class GfxAnticMode4FontConfigurationWidget(QWidget):
    pass

class GfxAnticMode4MultipleFonts(GfxABC):
    def getPixel(self, x, y):
        pass

    def putPixel(self, x, y, color_register_index):
        pass

    def modeName(self):
        return "Tiled, 128*2 tiles, 4+1 colors"

    def initFromMemory(self):
        pass

    def initLocally(self):
        pass


    def __init__(self):
        self.fonts = list()
        self.fonts.append(MemoryBuffer(1024))
        self.fonts.append(MemoryBuffer(1024))
        self.fonts.append(MemoryBuffer(1024))

