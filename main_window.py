from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from emulator_window import EmuWindow
from gfx_editor_window import GfxEditorWindow
from scene_view_window import SceneWindow
from playfield_editor_window import PlayfieldEditorWindow
from tileset_editor_window import TilesetEditorWindow
from console_window import ConsoleWindow
from palette_editor import PaletteEditorWindow
from console import console

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createMenuActions()
        self.createMenus()
        self.createDockWindows()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()
        self.setWindowTitle("Unity 8b (Singularity)")

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def readSettings(self):
        settings = QSettings("Unity8b.cfg", QSettings.IniFormat)
        geometry = settings.value("geometry");
        windowState = settings.value("windowState")
        if geometry is not None:
            self.restoreGeometry(geometry)
        if windowState is not None:
            self.restoreState(windowState)

    def writeSettings(self):
        settings = QSettings("Unity8b.cfg", QSettings.IniFormat)
        settings.setValue("geometry", self.saveGeometry());
        settings.setValue("windowState", self.saveState());

    def newGame(self):
        print("newGame")
        reply = QMessageBox.question(self, 'Message',
                                           "Sample Message", QMessageBox.Yes |
                                           QMessageBox.No, QMessageBox.No)
        pass

    def save(self):
        pass

    def undo(self):
        #document = self.textEdit.document()
        #document.undo()
        pass


    def about(self):
        QMessageBox.about(self, "About Unity 8b",
                "<b>Unity 8b</b> is a game development environment for 8bit computers (currently Atari 8bit).\n"
                "It is heavily inspired by Unity 3D by Unity Technologies but is not related to work of this company.\n"
                "Developed by Jakub 'ilmenit' Debski")

    def createMenuActions(self):
        self.newGameAct = QAction(QIcon(':/icons/new.png'), "&New Game",
                                  self, shortcut=QKeySequence.New,
                                  statusTip="Create a new game", triggered=self.newGame)

        self.saveAct = QAction(QIcon(':/icons/save.png'), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.save)

        self.undoAct = QAction(QIcon(':/icons/undo.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)


        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newGameAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newGameAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.undoAct)

        self.emuToolBar = self.addToolBar("Emu")
        self.emuToolBar.addAction(self.emulator.emuPlayAct)
        self.emuToolBar.addAction(self.emulator.emuPauseAct)
        self.emuToolBar.addAction(self.emulator.emuNextFrameAct)
        self.emuToolBar.addAction(self.emulator.emuStopAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        pass

    def createDockWindows(self):
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks)
        self.scene = SceneWindow(self)
        self.emulator = EmuWindow(self)
        self.gfxEditor = GfxEditorWindow(self)
        self.playfieldEditor = PlayfieldEditorWindow(self)
        self.tilesetEditor = TilesetEditorWindow(self)
        self.console = ConsoleWindow(self)
        self.paletteEditor = PaletteEditorWindow(self)
        console.init(self.console)

    def closeEvent_______________________(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Confirm closing', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()