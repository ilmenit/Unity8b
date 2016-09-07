from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from gfx_abc import *
from indexed_palette import *

class MemoryBuffer(QObject):
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

    def __init__(self, parent=None, data=None, address=None):
        super().__init__()
        self.data = data
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
        return 0

    def putPixel(self, x, y, color_register_index):
        pass

    def modeName(self):
        return "Tiled, 128*2 tiles, 4+1 colors"

    def initFromMemory(self):
        pass

    def initLocally(self):
        pass

    def toQImage(self):
        image = QImage(self.width,self.height, QImage.Format_RGB32)
        for y in range(self.height):
            for x in range(self.width):
                register_index = self.getPixel(x,y)
                color_value = self.color_registers[register_index]
                rgb_color = global_indexed_palette[color_value]
                image.setPixel(x,y,rgb_color.rgb())
        return image

    def __init__(self, width, height):
        super().__init__()
        self.color_registers = PlayfieldPalette()
        self.width = width
        self.height = height
        self.fonts = list()
        self.fonts.append(MemoryBuffer(1024))
        self.fonts.append(MemoryBuffer(1024))


class GfxIndexedTest(GfxABC):
    def getPixel(self, x, y):
        color_register_index = self.memory_buffer[y * self.width + x]
        return color_register_index

    def putPixel(self, x, y, color_register_index):
        self.memory_buffer[y * self.width + int(x/self.pixel_width_ration)] = color_register_index

    def modeName(self):
        return "SimpleIndexed"

    def getState(self):
        for_undo!
        pass

    def setState(self):
        pass

    def toQImage(self):
        image = QImage(self.width,self.height, QImage.Format_RGB32)
        for y in range(self.height):
            for x in range(self.width):
                register_index = self.getPixel(x,y)
                color_value = self.playfield_palette[register_index]
                rgb_color = global_indexed_palette[color_value]
                image.setPixel(x,y,rgb_color.rgb())

        size = image.size()
        return image.scaled(size.width()*self.pixel_width_ration,size.height(), Qt.IgnoreAspectRatio, Qt.FastTransformation)

    def setPalette(self, palette):
        self.playfield_palette = palette

    def __init__(self, width, height, pixel_width_ration=1):
        super().__init__()
        self.memory_buffer = bytearray(width * height)
        self.pixel_width_ration = 2
        self.width = width
        self.height = height
        self.image = QImage(self.width,self.height, QImage.Format_RGB32)