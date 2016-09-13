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
import collections
from copy import deepcopy
from utils import *

class GfxIndexedState():
    def __init__(self):
        self.width = 4
        self.height = 8
        self.pixel_width_ratio = 2
        self.memory_buffer = bytearray(self.width * self.height)

class GfxIndexedAsset(GfxAsset):

    playfield_palette = None

    @classmethod
    def typeName(cls):
        return "Indexed Gfx Test"

    def compile(self):
        raise NotImplementedError()

    def createEmptyState(self):
        return GfxIndexedState()

    @classmethod
    def fileExtensions(cls):
        return [ '.gfx' ]

    def moveToAssets(self):
        raise NotImplementedError()

    def openInEditor(self):
        inspect_call_args()
        print("SELF: " + str(self))
        singletons.main_window.gfxEditorWindow.setAsset(self)

    def placeOnScene(self):
        raise NotImplementedError()

    def getPixel(self, x, y):
        if self.state is None:
            return None
        if x<0 or x>=self.state.width or y<0 or y>=self.state.height:
            return None
        color_register_index = self.state.memory_buffer[y * self.state.width + x]
        return color_register_index

    def putPixel(self, x, y, color_register_index):
        x = int(x / self.state.pixel_width_ratio)
        if x<0 or x>=self.state.width or y<0 or y>=self.state.height:
            return
        self.state.memory_buffer[y * self.state.width + x] = color_register_index
        self.data_changed.emit()

    def modeName(self):
        return "SimpleIndexed"

    def getState(self):
        return deepcopy(self.state)

    def setState(self, state):
        self.state = deepcopy(state)
        self.data_changed.emit()

    def toQImage(self):
        if self.playfield_palette is None:
            self.playfield_palette = AssetPlayfieldPalette.createEmptyState()
        image = QImage(self.state.width,self.state.height, QImage.Format_RGB32)
        for y in range(self.state.height):
            for x in range(self.state.width):
                register_index = self.getPixel(x,y)
                color_value = self.playfield_palette.data[register_index]
                rgb_color = global_indexed_palette[color_value]
                image.setPixel(x,y,rgb_color.rgb())

        size = image.size()
        return image.scaled(size.width()*self.state.pixel_width_ratio,size.height(), Qt.IgnoreAspectRatio, Qt.FastTransformation)

    def setPalette(self, palette):
        self.playfield_palette = palette
        self.playfield_palette.dataChanged.connect(self.data_changed)


from project_platform import *
from asset_playfield_palette import *
