from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import *
from asset import *
from console import *

class AssetsTree(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

    def dataChangedHandler(self):
        inspect_call_args()
        self.sortByColumn(0, Qt.AscendingOrder)

    def changeEvent(self, *args, **kwargs): # real signature unknown
        self.dataChangedHandler()


class AssetsWindow(DockWindow):

    def fileActivated(self, index):
        path = self.dir_model.fileInfo(index).filePath()
        dir = QDir(self.dir_model.rootPath())
        relative_path = dir.relativeFilePath(path)
        print("Double Clicked " + str(relative_path))
        asset = self.parent().assets.load_file(path)
        if asset is None:
            console.error("Cannot load asset: " + path)
        else:
            asset.openInEditor()


    def loadFileHandler(self, file_name):
        print("Loading file " + file_name)

    def __init__(self, parent):
        super().__init__("Assets", parent)
        self.dir_model = QFileSystemModel()
        self.dir_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.AllEntries)
        self.dir_model.setReadOnly(False)

        self.assets_tree = AssetsTree(self)
        self.assets_tree.setModel(self.dir_model)
        root = self.dir_model.setRootPath(parent.project.path)
        self.assets_tree.setRootIndex(root)
        self.assets_tree.setSortingEnabled(True)
        self.assets_tree.sortByColumn(0, Qt.AscendingOrder)
        #self.dir_view.setWindowTitle("Dir View")
        self.assets_tree.hideColumn(1)
        self.assets_tree.hideColumn(2)
        self.assets_tree.hideColumn(3)
        self.assets_tree.header().setVisible(False)
        self.assets_tree.show()
        self.assets_tree.activated.connect(self.fileActivated)
        self.assets_tree.clicked.connect(self.fileActivated)
        self.assets_tree.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.setWidget(self.assets_tree)

