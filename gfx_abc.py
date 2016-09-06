'''
This is an abstract base class for pixel level operations on different graphics modes

Modes have:
- different encoding of pixels into memory representation
-
'''

from abc import ABCMeta, abstractmethod

class Size():
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

Position = Size

class PaletteColorABC(metaclass=ABCMeta):
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

class GfxABC(metaclass=ABCMeta):
    @abstractmethod
    def getPixel(self, x, y):
        pass

    @abstractmethod
    def putPixel(self, x, y, color_register_index):
        pass

    @abstractmethod
    def modeName(self):
        return "ModeName"



