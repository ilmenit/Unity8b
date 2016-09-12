from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from collections.abc import Sequence
from collections import OrderedDict
from asset import *
from memory_buffer import *
from singletons import main_window
import singletons
from utils import *

class AssetPlayfieldPalette(Asset):
    '''
    Playfield palette is an array of color
    '''

    data = None

    @trace
    def __init__(self, name, state, is_file=False, on_scene=False):
        super().__init__(name,state,is_file,on_scene)


    @classmethod
    def fileExtensions(cls):
        return [ '.pal' ]

    @classmethod
    def typeName(cls):
        return "Playfield Palette"

    def compile(self):
        print("PlayfieldPalette::compile")
        pass

    @trace
    @classmethod
    def createEmptyState(cls):
        state = MemoryBuffer(5)
        for i in range(len(state)):
            state[i] = i * 16 +5
        return state

    def placeOnScene(self):
        print("PlayfieldPalette::placeOnScene")
        pass

    def openInEditor(self):
        print("PlayfieldPalette::openInEditor")
        singletons.main_window.paletteEditorWindow.setAsset(self)

    def moveToAssets(self):
        print("PlayfieldPalette::moveToAssets")
        pass

    def getState(self):
        print("PlayfieldPalette::getState")
        return self.data.getState()

    @trace
    def setState(self, state):
        if self.data is None:
            self.data = self.createEmptyState()
        return self.data.setState(state)

from project_platform import *
