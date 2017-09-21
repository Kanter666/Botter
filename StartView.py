from Models.Library import Library

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog

qtViewFile = "./Design/Start.ui"  # Enter file here.

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class StartView(QtWidgets.QMainWindow, Ui_StartWindow):

    clicked_record = pyqtSignal()
    clicked_create = pyqtSignal()
    clicked_load = pyqtSignal(list)

    def __init__(self):
        self.box = 0

        QtWidgets.QMainWindow.__init__(self)
        Ui_StartWindow.__init__(self)
        self.setupUi(self)

        self.load_library_bt.clicked.connect(self.onclicked_load)
        self.create_library_bt.clicked.connect(self.clicked_create.emit)
        self.record_game_bt.clicked.connect(self.clicked_record.emit)

    def onclicked_load(self):
        library, _ = QFileDialog.getOpenFileName(
            self,
            "Select file of library that you want to load",
            "./",
            "Python Files (*.py)"
        )
        directory, functions, dictionary = Library.load_library(library)
        self.clicked_load.emit([directory, library, functions, dictionary])
