from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import *
from asset import *
from console import *
class AssetsWindow(DockWindow):

    def dirViewClicked(self, index):
        path = self.dir_model.fileInfo(index).filePath()
        dir = QDir(self.dir_model.rootPath())
        path = dir.relativeFilePath(path)
        print("Double Clicked " + str(path))
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
        #model.setReadOnly(False)

        self.dir_view = QTreeView()
        self.dir_view.setModel(self.dir_model)
        root = self.dir_model.setRootPath(parent.project.path)
        self.dir_view.setRootIndex(root)
        self.dir_view.setSortingEnabled(True)
        self.dir_view.sortByColumn(0, Qt.AscendingOrder)
        #self.dir_view.setWindowTitle("Dir View")
        self.dir_view.hideColumn(1)
        self.dir_view.hideColumn(2)
        self.dir_view.hideColumn(3)
        self.dir_view.header().setVisible(False)
        self.dir_view.show()
        self.dir_view.doubleClicked.connect(self.dirViewClicked)
        self.setWidget(self.dir_view)

