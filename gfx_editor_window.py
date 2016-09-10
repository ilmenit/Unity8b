from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
from gfx_atari import *
from asset_playfield_palette import *
from asset import *

class GfxEditorWindow(DockWindow):

    def resizeEvent(self, QResizeEvent):
        if self.gfx is not None:
            self.view.scaleToContent()

    def dataChangedHandler(self):
        self.pixmapItem.setPixmap(QPixmap.fromImage(self.gfx.toQImage()))

    def mousePressedHandler(self, point):
        self.old_state = self.gfx.getState()
        color_index = self.parent().paletteEditorWindow.selected_color
        self.gfx.putPixel(int(point.x()), int(point.y()),color_index)

    def mouseMovedHandler(self, point):
        color_index = self.parent().paletteEditorWindow.selected_color
        self.gfx.putPixel(int(point.x()), int(point.y()),color_index)

    def mouseReleasedHandler(self):
        new_state = self.gfx.getState()
        command = CommandChangeAsset(self.gfx, self.old_state, new_state)
        self.undoStack.push(command)

    def saveOnExit(self):
        if self.wasModified:
            reply = QMessageBox.question(self, 'GfxEditor',
                                     "The graphics has been modified. Do you want to store it?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

    def setGfx(self, gfx):
        print("GfxEditorWindow::setGfx")
        if self.gfx is not None:
            self.gfx.data_changed.disconnect(self.dataChangedHandler)
        self.gfx = gfx
        if gfx is not None:
            self.pixmap = QPixmap.fromImage(self.gfx.toQImage())
            self.scene = GridScene(self, self.gfx.width,self.gfx.height, self.gfx.pixel_width_ration)
            self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.pixmapItem)
            self.scene.createGrid()
            self.gfx.data_changed.connect(self.dataChangedHandler)
            self.dataChangedHandler()
            self.view = MyGraphicsView(self.scene)

            # connect slots and signalds
            self.view.mouse_pressed.connect(self.mousePressedHandler)
            self.view.mouse_moved.connect(self.mouseMovedHandler)
            self.view.mouse_released.connect(self.mouseReleasedHandler)
            self.setWidget(self.view)
        else:
            self.setWidget(QWidget())



    def __init__(self, parent):
        super().__init__("GfxEditor", parent)
        self.gfx = None
        self.old_state = None
        self.setGfx(None)

