from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from gfx_abc import *
from indexed_palette import *
from copy import copy
from memory_buffer import *

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


class GfxIndexedTest(GfxABC, metaclass=FinalMetaclass):

    def getPixel(self, x, y):
        if x<0 or x>=self.width or y<0 or y>=self.height:
            return
        color_register_index = self.memory_buffer[y * self.width + x]
        return color_register_index

    def putPixel(self, x, y, color_register_index):
        x = int(x / self.pixel_width_ration)
        if x<0 or x>=self.width or y<0 or y>=self.height:
            return
        self.memory_buffer[y * self.width + x] = color_register_index
        self.state_changed.emit()

    def modeName(self):
        return "SimpleIndexed"

    def getState(self):
        return copy(self.memory_buffer)

    def setState(self, state):
        self.memory_buffer = copy(state)
        self.state_changed.emit()

    def toQImage(self):
        image = QImage(self.width,self.height, QImage.Format_RGB32)
        palette_data = self.playfield_palette.getState()
        for y in range(self.height):
            for x in range(self.width):
                register_index = self.getPixel(x,y)
                color_value = palette_data[register_index]
                rgb_color = global_indexed_palette[color_value]
                image.setPixel(x,y,rgb_color.rgb())

        size = image.size()
        return image.scaled(size.width()*self.pixel_width_ration,size.height(), Qt.IgnoreAspectRatio, Qt.FastTransformation)

    def setPalette(self, palette):
        self.playfield_palette = palette

    def __init__(self, width, height, pixel_width_ration=1):
        super().__init__()
        self.memory_buffer = bytearray(width * height)
        self.pixel_width_ration = pixel_width_ration
        self.width = width
        self.height = height
        self.name = "sample picture"
        self.image = QImage(self.width,self.height, QImage.Format_RGB32)