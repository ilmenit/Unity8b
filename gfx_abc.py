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
    def __init__(self):
        self.x = x

class GfxABC(metaclass=ABCMeta):
    @abstractmethod
    def getPixel(self, color_register):
        pass

    @abstractmethod
    def putPixel(self, color_register):
        pass

    @abstractmethod
    def modeName(self):
        return "ModeName"

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

a = Size(10,20)
b = Position(20,30)
print("A: " + str(a))
print("B: " + str(b))

'''
How it works:
- In
'''