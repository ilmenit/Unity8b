from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dock_window import DockWindow

class IntField(QWidget):
    '''
    This widget is responsible for editing bytes as integer of defined length
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.setBytes(20)

    def setBytes(self, value, min_value=0, max_value=255):
        '''
        current parameters are for the demo. Memory view and size should be passed.
        '''
        self.layout = QHBoxLayout()
        self.name = QLabel("variable_name:")
        self.spin = QSpinBox()
        self.spin.setValue(value)
        self.spin.setMaximum(max_value)
        self.spin.setMinimum(min_value)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.spin)
        self.setLayout(self.layout)


class ObjectInspector(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObject()

    def setObject(self):
        self.setTitle("Test object")
        #self.setStyleSheet("QGroupBox::title {subcontrol-position: left, top;}")

        self.layout = QVBoxLayout()
        self.layout.addWidget(IntField(self))
        self.layout.addWidget(IntField(self))
        self.layout.addWidget(IntField(self))
        self.setLayout(self.layout)




class InspectorWindow(DockWindow):

    def __init__(self, parent):
        super().__init__("Inspector", parent)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setWidget(self.main_widget)

        self.main_layout.addWidget(ObjectInspector(self.main_widget))
        self.main_layout.addWidget(ObjectInspector(self.main_widget))
