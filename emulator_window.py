from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dock_window import DockWindow

class EmuWindow(DockWindow):
    def __init__(self, parent):
        super().__init__("Emulator", parent)
        self.textEdit = QTextEdit(self)
        self.setWidget(self.textEdit)

        self.emuPlayAct = QAction(QIcon(':/icons/play.png'), "&Play",
                              self, statusTip="Play emulator", triggered=self.play)

        self.emuPauseAct = QAction(QIcon(':/icons/pause.png'), "&Pause", self,
                               statusTip="Pause emulator", triggered=self.pause)

        self.emuNextFrameAct = QAction(QIcon(':/icons/next-frame.png'), "&Next Frame", self,
                                   statusTip="Next frame", triggered=self.nextFrame)

        self.emuStopAct = QAction(QIcon(':/icons/stop.png'), "&Stop", self,
                              statusTip="Stop emulator", triggered=self.stop)


    def play(self):
        print("Emu play")
        pass


    def pause(self):
        print("Emu pause")
        pass


    def nextFrame(self):
        print("Emu next frame")
        pass


    def stop(self):
        print("Emu stop ")
        pass