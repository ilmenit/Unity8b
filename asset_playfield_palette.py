from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from collections.abc import Sequence
from collections import OrderedDict
from asset import *
from memory_buffer import *
from singletons import main_window
import singletons

class AssetPlayfieldPalette(Asset):
    '''
    Playfield palette is an array of color
    '''
    type_name = "Playfield Palette"

    def __init__(self, name, memory_view = None):
        super().__init__(name)
        if memory_view is None:
            self.data = MemoryBuffer(5)
            for i in range(len(self.data)):
                self.data[i] = i * 16 + 5
        else:
            self.setState(memory_view)

    @classmethod
    def supportedPlatforms(cls):
        return [ PlatformAtariXl ]

    @classmethod
    def file_extensions(cls):
        return [ '.pal' ]

    def compile(self):
        print("PlayfieldPalette::compile")
        pass

    def placeOnScene(self):
        print("PlayfieldPalette::placeOnScene")
        pass

    def openInEditor(self):
        print("PlayfieldPalette::openInEditor")
        singletons.main_window.paletteEditorWindow.setPalette(self)

    def moveToAssets(self):
        print("PlayfieldPalette::moveToAssets")
        pass

    def getState(self):
        print("PlayfieldPalette::getState")
        return self.data.getState()

    def setState(self, state):
        print("PlayfieldPalette::setState")
        return self.data.setState(state)

from project_platform import *