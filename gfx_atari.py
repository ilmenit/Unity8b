from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from gfx_abc import *
from indexed_palette import *
from copy import copy
from memory_buffer import *
from asset import *

class GfxIndexedTest(GfxABC):

    @classmethod
    def typeName(cls):
        return "Indexed Gfx Test"

    def compile(self):
        raise NotImplementedError()

    @classmethod
    def file_extensions(cls):
        return [ '.mic' ]

    def moveToAssets(self):
        raise NotImplementedError()

    def openInEditor(self):
        singletons.main_window.gfxEditorWindow.setGfx(self)
        raise NotImplementedError()

    def placeOnScene(self):
        raise NotImplementedError()

    def __init__(self, name, width=4, height=8, pixel_width_ration=2):
        super().__init__(name=name)
        self.memory_buffer = bytearray(width * height)
        self.pixel_width_ration = pixel_width_ration
        self.width = width
        self.height = height
        self.name = "sample picture"
        self.image = QImage(self.width,self.height, QImage.Format_RGB32)

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
        self.data_changed.emit()

    def modeName(self):
        return "SimpleIndexed"

    def getState(self):
        return copy(self.memory_buffer)

    def setState(self, state):
        self.memory_buffer = copy(state)
        self.data_changed.emit()

    def toQImage(self):
        image = QImage(self.width,self.height, QImage.Format_RGB32)
        for y in range(self.height):
            for x in range(self.width):
                register_index = self.getPixel(x,y)
                color_value = self.playfield_palette.data[register_index]
                rgb_color = global_indexed_palette[color_value]
                image.setPixel(x,y,rgb_color.rgb())

        size = image.size()
        return image.scaled(size.width()*self.pixel_width_ration,size.height(), Qt.IgnoreAspectRatio, Qt.FastTransformation)

    def setPalette(self, palette):
        self.playfield_palette = palette
        self.playfield_palette.dataChanged.connect(self.data_changed)

