from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dock_window import DockWindow
import gfx_abc
from gfx_atari import *

class MyGraphicsView(QGraphicsView):
    mouse_pressed = pyqtSignal(QPointF, name="mousePressed")
    mouse_moved = pyqtSignal(QPointF, name="mouseMoved")
    mouse_released = pyqtSignal(name="mouseReleased")

    def showEvent(self, QShowEvent):
        self.scaleToContent()

    def scaleToContent(self):
        self.resetTransform()
        scale_x = self.width() / self.scene.width()
        scale_y = self.height() / self.scene.height()
        scale = min(scale_x,scale_y)
        scale -= scale/20
        self.scale(scale, scale)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.scene = scene

    def actionEvent(self, event):
        print("Action event " + str(event))

    def moveEvent(self, event):
        print("moveEvent event " + str(event))

    def mousePressEvent(self, event):
        pt = self.mapToScene(event.pos())
        print("mousePressEvent event " + str(event))
        #print("pt " + str(pt))
        self.mouse_pressed.emit(pt)

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent event " + str(event))
        self.mouse_released.emit()

    def mouseMoveEvent(self, event):
        #print("mouseMoveEvent event " + str(event))
        pt = self.mapToScene(event.pos())
        self.mouse_moved.emit(pt)

    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

class MyScene(QGraphicsScene):
    def createGrid(self):
        # dc.setCompositionMode(QPainter::RasterOp_SourceXorDestination);
        transparentLine = QPen(QColor(0x40, 0x40, 0x40, 0x80), 1, Qt.DotLine)
        for x in range(1, int(self.width()), 50):
            self.addLine(x - 0.5, 0.5, x - 0.5, int(self.height()), transparentLine)

        for y in range(1, int(self.height()), 50):
            self.addLine(0.5, y - 0.5, int(self.width()), y - 0.5, transparentLine)

    def __init__(self, parent):
        super().__init__(parent)

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
        self.gfx = GfxIndexedTest(4, 8,2)
        palette = PlayfieldPalette()
        self.old_state = None
        self.gfx.setPalette(palette)
        self.parent().paletteEditorWindow.setPalette(palette)
        self.pixmap = QPixmap.fromImage(self.gfx.toQImage())
        self.scene = MyScene(self)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        #self.scene.createGrid()
        self.view = MyGraphicsView(self.scene)
        self.setWidget(self.view)

        # connect slots and signalds
        self.gfx.state_changed.connect(self.update)
        self.view.mouse_pressed.connect(self.mousePressedHandler)
        self.view.mouse_moved.connect(self.mouseMovedHandler)
        self.view.mouse_released.connect(self.mouseReleasedHandler)
