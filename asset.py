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

class FinalMetaclass(pyqtWrapperType, ABCMeta):
    pass

class Asset(QObject, metaclass=FinalMetaclass):

    type_name = "Asset Name"
    onScene = False
    file_name = ''
    relativePath = '/'

    @classmethod
    def make_new_name(cls, file_name, extension):
        full_name = file_name + '.' + extension
        counter = 0
        while os.path.exists(full_name):
            counter += 1
            full_name = file_name + str(counter) + '.' + extension
        return full_name

    @classmethod
    @abstractmethod
    def supportedPlatforms(cls):
        pass

    @classmethod
    def createNew(cls, asset_type, name, project_path):
        file_name = os.path.join(project_path,"New " + name)
        extension = asset_type.file_extensions()[0]
        new_asset = asset_type()
        new_name = cls.make_new_name(file_name,extension)
        new_asset.save_to_file(new_name)
        return new_name

    @classmethod
    @abstractmethod
    def file_extensions(cls):
        pass

    @abstractmethod
    def compile(self):
        pass

    @abstractmethod
    def placeOnScene(self):
        pass

    @abstractmethod
    def openInEditor(self):
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
        self.file_name = file_name
        f = open(self.file_name, 'rb')
        if not f:
            console.error("Cannot open file for reading " + self.ile_name)
            return
        try:
            state = pickle.load(f)
        except:
            console.error("Cannot load file " + self.file_name)
            return
        self.setState(state)

    def save_to_file(self, file_name):
        self.file_name = file_name
        state = self.getState()
        f = open(self.file_name, 'wb')
        if not f:
            console.error("Cannot open file for writing " + self.file_name)
            return
        try:
            pickle.dump(state, f)
        except:
            console.error("Cannot save file " + self.file_name)
            return


class CommandChangeAsset(QUndoCommand):
    def __init__(self, asset, old_state, new_state):
        super().__init__("Change " + asset.name)
        self.asset = asset
        self.new_state = new_state
        self.old_state = old_state

    def redo(self):
        print("CommandChangeAsset::REDO " + self.asset.name)
        self.asset.setState(self.new_state)

    def undo(self):
        print("CommandChangeAsset::UNDO " + self.asset.name)
        self.asset.setState(self.old_state)


class Assets():
    def init_file_extensions(self):
        for asset in self.platform.supported_assets:
            for extension in asset.file_extensions():
                if extension in self.extension_mapping:
                    console.error("Extension " + str(extension) + " is already assigned to " + repr(self.extension_mapping[extension]))
                else:
                    self.extension_mapping[extension.lower()] = asset

    def __init__(self, project_platform):
        self.platform = project_platform
        self.extension_mapping = dict()
        self.init_file_extensions()

    def load_file(self, file_name):
        extension = os.path.splitext(file_name)[1].lower()
        if extension in self.extension_mapping:
            asset_class = self.extension_mapping[extension]
            asset_instance = asset_class()
            return asset_instance
        return None

    def edit_file(self, file_name):
        asset_instance = self.load_file(file_name)
        if asset_instance is not None:
            asset_instance.openInEditor()

