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
from asset import *
from asset_playfield_palette import *

default_tileset = {
    # "file_name" : "default.fnt",
    "file_name" : 'examples/shooter/default.fnt',
    "tiles_count" : 128,
    "tile_size_x" : 4,
    "tile_size_y" : 8,
    "tiles_height" : 3,
    "fonts" : array('B'),
}



class TilesetWidget(QWidget):

    def dataChangedHandler(self):
        print("TilesetWidget::dataChangedHandler")
        self.pixmapItem.setPixmap(QPixmap.fromImage(self.gfx.toQImage()))

    def __init__(self,parent):
        super().__init__(parent)
        self.gfx = None
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
        self.gfx.data_changed.connect(self.dataChangedHandler)
        #self.view.mouse_pressed.connect(self.mousePressedHandler)
        #self.view.mouse_moved.connect(self.mouseMovedHandler)
        #self.view.mouse_released.connect(self.mouseReleasedHandler)

class TilesetEditorWindow(DockWindow):

    def setAsset(self, asset):
        print("GfxEditorWindow::setGfx")
        if self.asset is not None:
            self.asset.data_changed.disconnect(self.dataChangedHandler)
        self.asset = asset
        if asset is not None:
            self.pixmap = QPixmap.fromImage(self.asset.toQImage())
            self.scene = GridScene(self, self.asset.width, self.asset.height, self.asset.pixel_width_ration)
            self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.pixmapItem)
            self.scene.createGrid()
            self.asset.data_changed.connect(self.dataChangedHandler)
            self.dataChangedHandler()
            self.view = MyGraphicsView(self.scene)

            # connect slots and signalds
            self.view.mouse_pressed.connect(self.mousePressedHandler)
            self.view.mouse_moved.connect(self.mouseMovedHandler)
            self.view.mouse_released.connect(self.mouseReleasedHandler)
            self.setWidget(self.view)
        else:
            self.setWidget(QWidget())

    def gfxModeChanged(self, i):
        print("GFX Mode Selected :" + str(i))
        console.info(i)


    def __init__(self, parent):
        super().__init__("Tileset Editor", parent)

