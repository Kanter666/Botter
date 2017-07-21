import sys

from PyQt5 import uic, QtWidgets
from CreateView import CreateView

qtViewFile = "./Design/Start.ui"  # Enter file here.

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)

class StartView(QtWidgets.QMainWindow, Ui_StartWindow):
    def __init__(self):
        self.box = 0

        QtWidgets.QMainWindow.__init__(self)
        Ui_StartWindow.__init__(self)
        self.setupUi(self)

        self.load_library_bt.clicked.connect(self.onclicked_load)

        self.create_library_bt.clicked.connect(self.onclicked_create)

    def onclicked_load(self):
        print("load")

    def onclicked_create(self):
        print("create")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StartView()
    window.show()
    sys.exit(app.exec_())
