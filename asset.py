'''
Each asset is:
- savable
- deployable on scene
- has type
- has data
- has dependencies on other assets
- has virtual dependencies on other assets (like gfx editor -> palette)
- has configuration window
- has editor window
'''

from abc import ABCMeta, abstractmethod
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from console import *
import pickle
import os
import singletons
from dock_window import DockWindow

class FinalMetaclass(pyqtWrapperType, ABCMeta):
    pass

class Asset(QObject, metaclass=FinalMetaclass):
    data_changed = pyqtSignal(name="dataChanged")
    on_scene = False
    is_file = False

    def __init__(self, name, state=None, is_file=False, on_scene=False):
        print("Asset::__init__")
        super().__init__()
        self.name = name
        self.on_scene = on_scene
        self.is_file = is_file
        if state is None:
            state = self.createEmptyState()
        self.setState(state)

    @classmethod
    def make_new_name(cls, file_name, extension):
        full_name = file_name + extension
        counter = 0
        while os.path.exists(full_name):
            counter += 1
            full_name = file_name + str(counter) + extension
        return full_name

    @classmethod
    @abstractmethod
    def createEmptyState(cls):
        pass

    @classmethod
    def createAsNewFile(cls, asset_type, name, project_path):
        file_name = os.path.join(project_path,"New " + name)
        extension = asset_type.fileExtensions()[0]
        new_name = cls.make_new_name(file_name,extension)
        new_asset = asset_type(new_name)
        new_asset.save_to_file(new_name)
        return new_name

    @classmethod
    @abstractmethod
    def fileExtensions(cls):
        pass

    @classmethod
    @abstractmethod
    def typeName(cls):
        pass

    @abstractmethod
    def compile(self):
        pass

    @abstractmethod
    def placeOnScene(self):
        pass

    @abstractmethod
    def openInEditor(self):
        '''
        Open the asset in internal or external editor
        '''
        pass

    @abstractmethod
    def moveToAssets(self):
        pass

    @abstractmethod
    def getState(self):
        pass

    @abstractmethod
    def setState(self, state):
        pass

    def load_from_file(self, file_name):
        '''
        Basic method to load state from file.
        If you want to support conversion from other format then in inherited class override this method
        and add conversion step to state
        '''
        print("Asset::load_from_file")
        self.name = file_name
        self.is_file = True
        f = open(self.name, 'rb')
        if not f:
            console.error("Cannot open file for reading " + self.ile_name)
            return
        try:
            state = pickle.load(f)
        except:
            console.error("Cannot load file " + self.name)
            return
        self.setState(state)

    def save_to_file(self, file_name):
        print("Asset::save_to_file")
        self.name = file_name
        self.is_file = True
        state = self.getState()
        f = open(self.name, 'wb')
        if not f:
            console.error("Cannot open file for writing " + self.name)
            return
        try:
            pickle.dump(state, f)
        except:
            console.error("Cannot save file " + self.name)
            return


class CommandChangeAsset(QUndoCommand):
    def __init__(self, asset, old_state, new_state):
        super().__init__("[" + asset.typeName() + "] " + asset.name)
        self.asset = asset
        self.new_state = new_state
        self.old_state = old_state

    def redo(self):
        #print("CommandChangeAsset::REDO " + self.asset.name)
        #print(str(self.new_state))
        self.asset.setState(self.new_state)
        if self.asset.is_file:
            self.asset.save_to_file()

    def undo(self):
        #print("CommandChangeAsset::UNDO " + self.asset.name)
        #print(str(self.old_state))
        self.asset.setState(self.old_state)
        if self.asset.is_file:
            self.asset.save_to_file()


class Assets():
    def init_file_extensions(self):
        for asset in singletons.main_window.project.platform.supported_assets:
            for extension in asset.fileExtensions():
                if extension in self.extension_mapping:
                    console.error("Extension " + str(extension) + " is already assigned to " + repr(self.extension_mapping[extension]))
                else:
                    self.extension_mapping[extension.lower()] = asset

    def __init__(self):
        self.extension_mapping = dict()
        self.init_file_extensions()

    def load_file(self, file_name):
        print("Assets::load_file")
        extension = os.path.splitext(file_name)[1].lower()
        if extension in self.extension_mapping:
            asset_class = self.extension_mapping[extension]
            asset_instance = asset_class(file_name, True)
            return asset_instance
        return None

    def edit_file(self, file_name):
        print("Assets::edit_file")
        asset_instance = self.load_file(file_name)
        if asset_instance is not None:
            asset_instance.openInEditor()


class AssetEditorWindow(DockWindow, metaclass=FinalMetaclass):
    data_changed = pyqtSignal(object, name='dataChanged')

    @classmethod
    @abstractmethod
    def windowName(self):
        pass

    @abstractmethod
    def setAsset(self, asset):
        pass

    @abstractmethod
    def dataChangedHandler(self):
        pass

    def __init__(self, parent):
        super().__init__(self.windowName(), parent)
