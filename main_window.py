from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from emulator_window import EmuWindow
from gfx_editor_window import GfxEditorWindow
from scene_view_window import SceneWindow
from playfield_editor_window import PlayfieldEditorWindow
from tileset_editor_window import TilesetEditorWindow
from console_window import ConsoleWindow
from palette_editor_window import PaletteEditorWindow
from color_picker_window import ColorPickerWindow
from undo_view_window import UndoViewWindow
from assets_window import AssetsWindow
from console import console
from project import *
from project import *
import singletons
from utils import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        singletons.main_window = self
        self.project = Project("Test project")
        self.assets = Assets()
        self.undoStack = QUndoStack(self)
        self.createMenuActions()
        self.createMenus()
        self.createDockWindows()
        self.createToolBars()
        self.createStatusBar()
        self.readSettings()
        # If Unity Tech. decide to ban it then we can always change name to sth. like "Singularity" ;-)
        self.setWindowTitle("Unity 8b")

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
        reply = QMessageBox.question(self, 'Message',
                                           "Sample Message", QMessageBox.Yes |
                                           QMessageBox.No, QMessageBox.No)
        pass

    def save(self):
        pass

    def undo(self):
        print("MainWindow::UNDO")
        self.undoStack.undo()

    def redo(self):
        print("MainWindow::REDO")
        self.undoStack.redo()


    def about(self):
        QMessageBox.about(self, "About Unity 8b",
                "<b>Unity 8b</b> is a game development environment for 8bit computers (currently Atari XL,XE, in the future: NES, C64, ZX Spectrum?).<br>"
                "It is inspired by Unity (<a href='http://www.unity3d.com'>link</a>) by Unity Technologies but is not related to work of this company.<br>"
                "Developed by Jakub 'ilmenit' Debski as a tribute to amazing 8bit designers of the eighties.")

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

        self.redoAct = QAction(QIcon(':/icons/redo.png'), "&Redo", self,
                shortcut=QKeySequence.Redo,
                statusTip="Redo the last editing action", triggered=self.redo)


        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.notImplementedAct = QAction("None", self,
                statusTip="Not implemented", triggered=self.notImplemented)


        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

    def notImplemented(self):
        pass

    def create_new_asset(self, asset_type):
        new_asset = Asset.createAsNewFile(asset_type, asset_type.typeName())
        file_name = new_asset.name
        print("file name " + file_name)
        new_index = self.assetsWindow.dir_model.index(file_name)
        print("New index " + str(new_index))
        self.assetsWindow.assets_tree.setCurrentIndex(new_index)
        self.assetsWindow.show()
        new_asset.openInEditor()

    def buildAssetsMenu(self, menu):
        inspect_call_args()

        for asset in self.project.platform.supported_assets:
            # binding is needed to make lambda work in loop properly explenation:
            # https://blog.mister-muffin.de/2011/08/14/python-for-loop-scope-and-nested-functions/
            # or http://stackoverflow.com/questions/19837486/python-lambda-in-a-loop
            def bind(x):
                return lambda: self.create_new_asset(x)
            action = QAction(asset.typeName(), self, statusTip="Create " + asset.typeName(), triggered=bind(asset))
            menu.addAction(action)

    def createMenus(self):

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newGameAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)

        self.assetsMenu = self.menuBar().addMenu("&Assets")
        self.createAssetsMenu = self.assetsMenu.addMenu("Create")
        self.buildAssetsMenu(self.createAssetsMenu)

        self.windowsMenu = self.menuBar().addMenu("&Windows")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newGameAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.undoAct)
        self.editToolBar.addAction(self.redoAct)

        self.emuToolBar = self.addToolBar("Emu")
        self.emuToolBar.addAction(self.emulatorWindow.emuPlayAct)
        self.emuToolBar.addAction(self.emulatorWindow.emuPauseAct)
        self.emuToolBar.addAction(self.emulatorWindow.emuNextFrameAct)
        self.emuToolBar.addAction(self.emulatorWindow.emuStopAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks)
        self.sceneWindow = SceneWindow(self)
        self.assetsWindow = AssetsWindow(self)
        self.emulatorWindow = EmuWindow(self)
        self.playfieldEditorWindow = PlayfieldEditorWindow(self)
        self.tilesetEditorWindow = TilesetEditorWindow(self)
        self.consoleWindow = ConsoleWindow(self)
        self.paletteEditorWindow = PaletteEditorWindow(self)
        self.colorPickerWindow = ColorPickerWindow(self)
        self.gfxEditorWindow = GfxEditorWindow(self)
        self.colorPickerWindow.color_picked.connect(self.paletteEditorWindow.changeSelectedColorRegister)
        self.paletteEditorWindow.inform_color_picker.connect(self.colorPickerWindow.activateColor)
        self.paletteEditorWindow.data_changed.connect(self.gfxEditorWindow.update)
        self.undoViewWindow = UndoViewWindow(self)

        console.init(self.consoleWindow)

    def closeEvent_______________________(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Confirm closing', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()