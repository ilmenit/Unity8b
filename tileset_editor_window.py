import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from array import *
from copy import deepcopy
from dock_window import DockWindow
from console import console
import gfx_abc
from gfx_atari import *
from asset_playfield_palette import *

default_tileset = {
    # "file_name" : "default.fnt",
    "file_name" : 'examples/arkanoid/default.fnt',
    "tiles_count" : 128,
    "tile_size_x" : 4,
    "tile_size_y" : 8,
    "tiles_height" : 3,
    "fonts" : array('B'),
}

class TilesetWidget(QWidget):

    def update(self):
        print("Update")

    def __init__(self,parent):
        super().__init__(parent)
        self.gfx = GfxIndexedTest(128*8, 8*3, 1)
        palette = AssetPlayfieldPalette("test")
        self.old_state = None
        self.gfx.setPalette(palette)
        self.pixmap = QPixmap.fromImage(self.gfx.toQImage())
        self.scene = GridScene(self, 8, 8*3, 1)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        self.view = MyGraphicsView(self.scene, self, False)
        self.scene.createGrid()

        mainVLayout = QVBoxLayout()
        mainVLayout.addWidget(self.view)
        self.setLayout(mainVLayout)

        # connect slots and signalds
        self.gfx.data_changed.connect(self.update)
        #self.view.mouse_pressed.connect(self.mousePressedHandler)
        #self.view.mouse_moved.connect(self.mouseMovedHandler)
        #self.view.mouse_released.connect(self.mouseReleasedHandler)

class TilesetEditorWindow(DockWindow):

    def save(self):
        pass

    def load(self):
        file_name = self.data['file_name']

        try:
            file_size = os.path.getsize(file_name)
        except OSError:
            console.error("Cannot open " + file_name)
            return

        if file_size % 8 != 0:
            console.error("Tile file size must be dividiable by 8")
            return

        print("Loading : " + file_name)
        with open(file_name, "rb") as f:
            new_data = array('B')
            new_data.fromfile(f, file_size)
            self.data['fonts'] = new_data

    def loadFileHandler(self):
        file_name = QFileDialog.getOpenFileName()
        self.data['file_name'] = file_name[0]
        self.load()

    def gfxModeChanged(self, i):
        print("GFX Mode Selected :" + str(i))
        console.info(i)

    def tabSettings(self):

        tab_settings = QWidget()
        mainVLayout = QVBoxLayout()

        # file selection
        fileSelection = QWidget()
        hBoxlayout1 = QHBoxLayout()
        file_name = QLineEdit()
        file_name.setReadOnly(True)
        pushButton1 = QPushButton("Load")

        pushButton1.clicked.connect(self.loadFileHandler)
        hBoxlayout1.addWidget(file_name)
        hBoxlayout1.addWidget(pushButton1)
        fileSelection.setLayout(hBoxlayout1)

        # graphics mode
        gfxMode = QWidget()
        hBoxlayout2 = QHBoxLayout()
        gfx_mode_label = QLabel("Gfx mode")
        gfx_combo_box = QComboBox()
        gfx_combo_box.addItems(['Text mode, 2 colors, 40 x 24','One','Two','Three'])
        gfx_combo_box.setEditable(False)
        gfx_combo_box.currentIndexChanged.connect(self.gfxModeChanged)
        hBoxlayout2.addWidget(gfx_mode_label)
        hBoxlayout2.addWidget(gfx_combo_box)
        gfxMode.setLayout(hBoxlayout2)

        pushButton2 = QPushButton("Something 1")
        pushButton3 = QPushButton("Something 2")
        mainVLayout.addWidget(fileSelection)
        mainVLayout.addWidget(gfxMode)
        mainVLayout.addWidget(pushButton3)
        tab_settings.setLayout(mainVLayout)
        return tab_settings

    def createTabs(self,parent):
        # add tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(TilesetWidget(self), "Editor")
        self.tabs.addTab(self.tabSettings(), "Settings")
        self.setWidget(self.tabs)

    def __init__(self, parent):
        super().__init__("Tileset Editor", parent)
        self.createTabs(parent)
        self.data = deepcopy(default_tileset)
        self.load()

