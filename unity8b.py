'''
Good examples:
- pixelator and scribble - as an FONT and GFX editor
- editable tree model - object hierarchy
- simple tree model -
'''

#!/usr/bin/env python
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import unity8b_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.readSettings()
        self.setWindowTitle("Unity 8b - 8bit version of Unity")

        self.newLetter()

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

    def newLetter(self):
        self.textEdit.clear()

        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)

        textFormat = QTextCharFormat()
        boldFormat = QTextCharFormat()
        boldFormat.setFontWeight(QFont.Bold)
        italicFormat = QTextCharFormat()
        italicFormat.setFontItalic(True)

        tableFormat = QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(16)
        tableFormat.setAlignment(Qt.AlignRight)
        cursor.insertTable(1, 1, tableFormat)
        cursor.insertText("The Firm", boldFormat)
        cursor.insertBlock()
        cursor.insertText("321 City Street", textFormat)
        cursor.insertBlock()
        cursor.insertText("Industry Park")
        cursor.insertBlock()
        cursor.insertText("Some Country")
        cursor.setPosition(topFrame.lastPosition())
        cursor.insertText(QDate.currentDate().toString("d MMMM yyyy"),
                textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Dear ", textFormat)
        cursor.insertText("NAME", italicFormat)   
        cursor.insertText(",", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("Yours sincerely,", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("The Boss", textFormat)
        cursor.insertBlock()
        cursor.insertText("ADDRESS", italicFormat)  

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return

        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def emuPlay(self):
        pass

    def emuPause(self):
        pass

    def emuStop(self):
        pass

    def insertCustomer(self, customer):
        if not customer:
            return
        customerList = customer.split(', ')
        document = self.textEdit.document()
        cursor = document.find('NAME')
        if not cursor.isNull():
            cursor.beginEditBlock()
            cursor.insertText(customerList[0])
            oldcursor = cursor
            cursor = document.find('ADDRESS')
            if not cursor.isNull():
                for i in customerList[1:]:
                    cursor.insertBlock()
                    cursor.insertText(i)
                cursor.endEditBlock()
            else:
                oldcursor.endEditBlock()

    def addParagraph(self, paragraph):
        if not paragraph:
            return
        document = self.textEdit.document()
        cursor = document.find("Yours sincerely,")
        if cursor.isNull():
            return
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor,
                2)
        cursor.insertBlock()
        cursor.insertText(paragraph)
        cursor.insertBlock()
        cursor.endEditBlock()

    def about(self):
        QMessageBox.about(self, "About Unity 8b",
                "<b>Unity 8b</b> is a game development environment for 8bit computers (currently Atari 8bit).\n"
                "It is heavily inspired by Unity 3D by Unity Technologies but is not related to work of this company.")

    def createActions(self):
        self.newLetterAct = QAction(QIcon(':/icons/new.png'), "&New Letter",
                self, shortcut=QKeySequence.New,
                statusTip="Create a new form letter", triggered=self.newLetter)

        self.saveAct = QAction(QIcon(':/icons/save.png'), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.save)

        self.undoAct = QAction(QIcon(':/icons/undo.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

        self.emuPlayAct = QAction(QIcon(':/icons/play.png'), "&Play",
                self, statusTip="Play emulator", triggered=self.emuPlay)

        self.emuPauseAct = QAction(QIcon(':/icons/pause.png'), "&Pause", self,
                statusTip="Pause emulator", triggered=self.emuPause)

        self.emuStopAct = QAction(QIcon(':/icons/stop.png'), "&Stop", self,
                statusTip="Stop emulator", triggered=self.emuStop)

        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newLetterAct)
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
        self.fileToolBar.addAction(self.newLetterAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.undoAct)

        self.emuToolBar = self.addToolBar("Emu")
        self.emuToolBar.addAction(self.emuPlayAct)
        self.emuToolBar.addAction(self.emuPauseAct)
        self.emuToolBar.addAction(self.emuStopAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createEmuWindow(self):
        dock = QDockWidget("Emu", self)
        dock.setObjectName("Emu")
        self.textEdit = QTextEdit(dock)
        dock.setWidget(self.textEdit)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def createHierarchyWindow(self):
        dock = QDockWidget("Customers", self)
        dock.setObjectName("Customers")
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.addItems((
            "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton",
            "Jane Doe, Memorabilia, 23 Watersedge, Beaton",
            "Tammy Shea, Tiblanka, 38 Sea Views, Carlton",
            "Tim Sheen, Caraba Gifts, 48 Ocean Way, Deal",
            "Sol Harvey, Chicos Coffee, 53 New Springs, Eccleston",
            "Sally Hobart, Tiroli Tea, 67 Long River, Fedula"))
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

    def createPropertiesWindow(self):
        dock = QDockWidget("Paragraphs", self)
        dock.setObjectName("Paragraphs")
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
                "28 days.",
            "We have dispatched those items that were in stock. The rest of "
                "your order will be dispatched once all the remaining items "
                "have arrived at our warehouse. No additional shipping "
                "charges will be made.",
            "You made a small overpayment (less than $5) which we will keep "
                "on account for you, or return at your request.",
            "You made a small underpayment (less than $1), but we have sent "
                "your order anyway. We'll add this underpayment to your next "
                "bill.",
            "Unfortunately you did not send enough money. Please remit an "
                "additional $. Your order will be dispatched as soon as the "
                "complete amount has been received.",
            "You made an overpayment (more than $5). Do you wish to buy more "
                "items, or should we return the excess to you?"))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        self.customerList.currentTextChanged.connect(self.insertCustomer)
        self.paragraphsList.currentTextChanged.connect(self.addParagraph)

    def createDockWindows(self):
        self.createHierarchyWindow()
        self.createPropertiesWindow()
        self.createEmuWindow()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
