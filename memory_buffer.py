from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from intervaltree import *
from copy import copy

class MemoryBuffer(QObject):
    data_changed = pyqtSignal(object, name='dataChanged')

    def __init__(self, size, state=None):
        super().__init__()
        if state is None:
            self.size = size
            self.data = bytearray(self.size)
        else:
            self.size = len(state)
            self.data = state
        self.view = memoryview(self.data)
        self.interval_tree = IntervalTree()

    def notify(self, start, end):
        #print("Memory Buffer Changed {:d}:{:d}".format(start,end))
        #print("Tree size " + str(len(self.interval_tree)))
        #print("Search s:{:d},e:{:d}".format(start,end))
        search_results = self.interval_tree.search(start, end)
        for interval in search_results:
            # print("View Changed " + str(interval.data.offset) + ":" + str(interval.data.size))
            interval.data.data_changed.emit(interval.data)
        # any change in view means change in the whole buffer
        self.data_changed.emit(self)

    def addView(self, view):
        #print("Adding view " + str(view) + " s:{:d},e:{:d}".format(view.offset,view.offset+view.size))
        interval = Interval(view.offset, view.offset + view.size, view)
        view.interval = interval
        self.interval_tree.add(interval)

    def removeView(self, view):
        self.interval_tree.remove(view.interval)

    def clearViews(self):
        self.interval_tree.clear()

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value
        self.notify(index,index+1)

    def getState(self):
        return copy(self.data)

    def setState(self, state):
        if len(state) != self.size:
            raise ValueError("Assigning state of wrong size")
        self.data[:] = state[:]
        self.notify(0, self.size)


class MemoryView(QObject):
    data_changed = pyqtSignal(object, name='dataChanged')

    def __init__(self, storage, offset, size, name=None):
        super().__init__()
        self.storage = storage
        self.offset = offset
        self.size = size
        self.end = self.offset + self.size
        self.name = name
        self.storage.addView(self)

    def getState(self):
        return bytearray(self.storage.view[self.offset:self.end])

    def setState(self, state):
        if len(state) != self.size:
            raise ValueError("Assigning state of wrong size")
        self.storage.view[self.offset:self.end] = state[:]
        # print("Setting state finished")
        self.storage.notify(self.offset, self.end)

    def __getitem__(self, index):
        return self.storage.view[self.offset + index]

    def __setitem__(self, index, value):
        self.storage[self.offset + index] = value

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.getState())


if __name__ == '__main__':
    def ReportObjectChanged(obj):
        print("Object changed: " + repr(obj))

    memory_buffer = MemoryBuffer(20)
    memory_buffer.data_changed.connect(ReportObjectChanged)
    view1 = MemoryView(memory_buffer, 0, 5, "View 1")
    view2 = MemoryView(memory_buffer, 2, 5, "View 2")
    view3 = MemoryView(memory_buffer, 0, 2, "View 3")
    view1.data_changed.connect(ReportObjectChanged)
    view2.data_changed.connect(ReportObjectChanged)
    view3.data_changed.connect(ReportObjectChanged)
    # memory_buffer[0] = 1
    view1[2] = 1
    print("Memory buffer:")
    print(str(memory_buffer))
    print("View1:")
    print(str(view1))
    print("View2:")
    print(str(view2))
    print("View3:")
    print(str(view3))
    print("Getting state")
    state = memory_buffer.getState()
    state[0] = 255
    print("Setting state")
    memory_buffer.setState(state)
    print("View3:")
    print(str(view3))
    view3.setState(bytearray(b'\x22\x33'))

    print("View1:")
    print(str(view1))
