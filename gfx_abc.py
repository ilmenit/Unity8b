'''
This is an abstract base class for pixel level operations on different graphics modes

Modes have:
- different encoding of pixels into memory representation
-
'''

from abc import ABCMeta, abstractmethod
from PyQt5.QtCore import *

class Size():
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

Position = Size

class FinalMetaclass(pyqtWrapperType, ABCMeta):
    pass

class PaletteColorABC(metaclass=FinalMetaclass):
    @abstractmethod
    def getRGB(self, index):
        pass

    @abstractmethod
    def setRGB(self, index, rgb):
        pass

class PlayfieldPalette():
    '''
    Set of color registers
    '''
    def __init__(self):
        self.x = x

class GfxABC(QObject, metaclass=FinalMetaclass):
    state_changed = pyqtSignal(name="stateChanged")

    @abstractmethod
    def getPixel(self, x, y):
        pass

    @abstractmethod
    def putPixel(self, x, y, color_register_index):
        pass

    @abstractmethod
    def modeName(self):
        return "ModeName"



