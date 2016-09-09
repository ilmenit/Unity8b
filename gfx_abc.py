'''
This is an abstract base class for pixel level operations on different graphics modes

Modes have:
- different encoding of pixels into memory representation
-
'''

from abc import ABCMeta, abstractmethod
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FinalMetaclass(pyqtWrapperType, ABCMeta):
    pass

class GfxABC(QObject, metaclass=FinalMetaclass):
    state_changed = pyqtSignal(name="stateChanged")

    @abstractmethod
    def getPixel(self, x, y):
        pass

    @abstractmethod
    def putPixel(self, x, y, color_register_index):
        pass

    @abstractmethod
    def modeName(self):
        return "ModeName"

    @abstractmethod
    def getState(self):
        pass

    @abstractmethod
    def setState(self, state):
        pass

    @abstractmethod
    def toQImage(self):
        pass

    @abstractmethod
    def setPalette(self, palette):
        pass


class MyGraphicsView(QGraphicsView):
    mouse_pressed = pyqtSignal(QPointF, name="mousePressed")
    mouse_moved = pyqtSignal(QPointF, name="mouseMoved")
    mouse_released = pyqtSignal(name="mouseReleased")

    def showEvent(self, QShowEvent):
        print("Scale to content")
        self.scaleToContent()

    def scaleToContent(self):
        self.resetTransform()
        if self.scale_content_to_y:
            scale = self.height() / self.scene.height()
        else:
            scale_x = self.width() / self.scene.width()
            scale_y = self.height() / self.scene.height()
            scale = min(scale_x,scale_y)
        scale -= scale/20
        self.scale(scale, scale)

    def __init__(self, scene, parent=None, scale_content_to_y=False):
        super().__init__(scene,parent)
        self.scene = scene
        self.scale_content_to_y = scale_content_to_y
        self.mouse_is_pressed = False
        self.setResizeAnchor(self.AnchorUnderMouse)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def actionEvent(self, event):
        print("Action event " + str(event))

    def moveEvent(self, event):
        print("moveEvent event " + str(event))

    def mousePressEvent(self, event):
        pt = self.mapToScene(event.pos())
        print("mousePressEvent event " + str(event))
        #print("pt " + str(pt))
        self.mouse_is_pressed = True
        self.mouse_pressed.emit(pt)

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent event " + str(event))
        self.mouse_is_pressed = False
        self.mouse_released.emit()

    def mouseMoveEvent(self, event):
        #print("mouseMoveEvent event " + str(event))
        super().mouseMoveEvent(event)
        if not self.mouse_is_pressed:
            return
        pt = self.mapToScene(event.pos())
        self.mouse_moved.emit(pt)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        self.scale(factor, factor)

class GridScene(QGraphicsScene):
    def createGrid(self):
        # dc.setCompositionMode(QPainter::RasterOp_SourceXorDestination);
        penRadius = 0.10
        pen1 = QPen(QColor(0x0, 0x0, 0x0, 0x80), penRadius*2, Qt.DotLine)
        pen1.setDashPattern([1,2])
        pen2 = QPen(QColor(0xF0, 0xF0, 0xF0, 0x80), penRadius*2, Qt.DotLine)
        pen2.setDashPattern([1,2])
        pen2.setDashOffset(1)
        for x in range(int(penRadius*2), int(self.width()), self.grid_x):
            self.addLine(x - penRadius, penRadius, x - penRadius, int(self.height()), pen1)
            self.addLine(x - penRadius, penRadius, x - penRadius, int(self.height()), pen2)

        for y in range(int(penRadius*2), int(self.height()), self.grid_y):
            self.addLine(penRadius, y - penRadius, int(self.width()), y - penRadius, pen1)
            self.addLine(penRadius, y - penRadius, int(self.width()), y - penRadius, pen2)

    def __init__(self, parent, grid_x, grid_y, pixel_width_ration):
        super().__init__(parent)
        self.grid_x = grid_x * pixel_width_ration
        self.grid_y = grid_y
