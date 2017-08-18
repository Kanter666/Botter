import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal

qtViewFile = "./Design/ScreenMapper.ui"  # Enter file here.

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)

class ScreenMapperView(QtWidgets.QMainWindow, Ui_StartWindow):

    clicked_cancel = pyqtSignal()

    def __init__(self):

        self.text = None

        QtWidgets.QMainWindow.__init__(self)
        Ui_StartWindow.__init__(self)
        self.setupUi(self)

        self.cancel_bt.clicked.connect(self.clicked_cancel.emit)
        self.finish_bt.clicked.connect(self.print_arguments)

    def set_arguments(self, arguments):
        self.text = arguments[0]

    def print_arguments(self):
        print(self.text)
