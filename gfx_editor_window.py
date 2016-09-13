from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
from gfx_atari import *
from asset import *

class GfxEditorWindow(AssetEditorWindow):

    def windowName(self):
        return "Gfx Editor"

    def resizeEvent(self, QResizeEvent):
        if self.asset is not None:
            self.view.scaleToContent()

    def dataChangedHandler(self):
        self.pixmapItem.setPixmap(QPixmap.fromImage(self.asset.toQImage()))

    def mousePressedHandler(self, point):
        self.old_state = self.asset.getState()
        color_index = self.parent().paletteEditorWindow.selected_color
        self.asset.putPixel(int(point.x()), int(point.y()), color_index)

    def mouseMovedHandler(self, point):
        color_index = self.parent().paletteEditorWindow.selected_color
        self.asset.putPixel(int(point.x()), int(point.y()), color_index)

    def mouseReleasedHandler(self):
        new_state = self.asset.getState()
        command = CommandChangeAsset(self.asset, self.old_state, new_state)
        self.undoStack.push(command)

    def saveOnExit(self):
        if self.wasModified:
            reply = QMessageBox.question(self, 'GfxEditor',
                                     "The graphics has been modified. Do you want to store it?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

    def setAsset(self, asset):
        inspect_call_args()
        super().setAsset(asset)
        if asset is not None:
            self.pixmap = QPixmap.fromImage(self.asset.toQImage())
            self.scene = GridScene(self, self.asset.state.width, self.asset.state.height, self.asset.state.pixel_width_ratio)
            self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.pixmapItem)
            self.scene.createGrid()
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
        super().__init__(parent)
        self.asset = None
        self.old_state = None
        self.setAsset(None)
