import sys
from PyQt5 import uic, QtWidgets
from  PyQt5.QtWidgets import QPushButton

qtViewFile = "./Design/Main.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.start_button.clicked.connect(self.onclicked_start)

        self.stop_button.clicked.connect(self.onclicked_stop)

    def onclicked_start(self):
        print("start")

    def onclicked_stop(self):
        print("stop")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
