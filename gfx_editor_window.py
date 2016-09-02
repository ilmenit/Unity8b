from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dock_window import DockWindow
import gfx_abc

class MyGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.scene = scene

        # dc.setCompositionMode(QPainter::RasterOp_SourceXorDestination);
        transparentLine = QPen(QColor(0x40, 0x40, 0x40, 0x80), 1, Qt.DotLine)

        for x in range(1, 500, 50):
            self.scene.addLine(x-0.5, 0.5, x-0.5, 500, transparentLine)

        for y in range(1, 500, 50):
            self.scene.addLine(0.5, y-0.5, 500, y-0.5, transparentLine)

    def actionEvent(self, event):
        print("Action event " + str(event))

    def moveEvent(self, event):
        print("moveEvent event " + str(event))

    def mousePressEvent(self, event):
        pt = self.mapToScene(event.pos())
        print("mousePressEvent event " + str(event))
        print("pt " + str(pt))

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent event " + str(event))

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent event " + str(event))


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

class GfxEditorWindow(DockWindow):
    def drawLine(self, x1, y1, x2, y2):
        # this is a test function
        print("self.pixmapItem : " + str(self.pixmapItem))
        pixmap = self.pixmapItem.pixmap()
        print("pixmap : " + str(pixmap))
        painter = QPainter()
        painter.begin(pixmap)
        pen = QPen(Qt.white)
        painter.setPen(pen)
        painter.drawLine(x1, y1, x2, y2)
        painter.end()
        self.pixmapItem.setPixmap(pixmap)
        print("Done")

    def saveOnExit(self):
        if self.wasModified:
            reply = QMessageBox.question(self, 'GfxEditor',
                                     "The graphics has been modified. Do you want to store it?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)


    def __init__(self, parent):
        super().__init__(parent,"GfxEditor")
        self.pixmap = QPixmap("examples/arkanoid/redrock.png")
        self.scene = QGraphicsScene(self)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmapItem)
        self.view = MyGraphicsView(self.scene)
        self.setWidget(self.view)

        # test
        self.drawLine(20,20,500,500)
