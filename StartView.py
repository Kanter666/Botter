from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal

qtViewFile = "./Design/Start.ui"  # Enter file here.

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)

class StartView(QtWidgets.QMainWindow, Ui_StartWindow):

    clicked_create = pyqtSignal()
    def __init__(self):
        self.box = 0

        QtWidgets.QMainWindow.__init__(self)
        Ui_StartWindow.__init__(self)
        self.setupUi(self)

        self.load_library_bt.clicked.connect(self.onclicked_load)

        self.create_library_bt.clicked.connect(self.clicked_create.emit)

    def onclicked_load(self):
        print("load")


    def onclicked_create(self):
        print("create")
