from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
import gfx_abc
from gfx_atari import *

class CommandModifyGfx(QUndoCommand):
    def __init__(self, gfx, old_state):
        super(CommandModifyGfx, self).__init__("ModifyGfx " + gfx.name)
        self.gfx = gfx
        self.value = gfx.getState()
        self.old_value = old_state

    def redo(self):
        print("CommandModifyGfx::REDO")
        self.gfx.setState(self.value)

    def undo(self):
        print("CommandModifyGfx::UNDO")
        self.gfx.setState(self.old_value)

class GfxEditorWindow(DockWindow):

    def resizeEvent(self, QResizeEvent):
        self.view.scaleToContent()

    def update(self):
        self.pixmapItem.setPixmap(QPixmap.fromImage(self.gfx.toQImage()))

    def mousePressedHandler(self, point):
        self.old_state = self.gfx.getState()
        color_index = self.parent().paletteEditorWindow.selected_color
        self.gfx.putPixel(int(point.x()), int(point.y()),color_index)

    def mouseMovedHandler(self, point):
        color_index = self.parent().paletteEditorWindow.selected_color
        self.gfx.putPixel(int(point.x()), int(point.y()),color_index)

    def mouseReleasedHandler(self):
        command = CommandModifyGfx(self.gfx, self.old_state)
        self.undoStack.push(command)

    def saveOnExit(self):
        if self.wasModified:
            reply = QMessageBox.question(self, 'GfxEditor',
                                     "The graphics has been modified. Do you want to store it?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)


    def __init__(self, parent):
        super().__init__("GfxEditor", parent)
        self.gfx = GfxIndexedTest(4, 8, 2)
        palette = PlayfieldPalette()
        self.old_state = None
        self.gfx.setPalette(palette)
        self.parent().paletteEditorWindow.setPalette(palette)
        self.pixmap = QPixmap.fromImage(self.gfx.toQImage())
        self.scene = GridScene(self, 8,8, 2)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        self.scene.createGrid()
        self.view = MyGraphicsView(self.scene)
        self.setWidget(self.view)

        # connect slots and signalds
        self.gfx.state_changed.connect(self.update)
        self.view.mouse_pressed.connect(self.mousePressedHandler)
        self.view.mouse_moved.connect(self.mouseMovedHandler)
        self.view.mouse_released.connect(self.mouseReleasedHandler)
