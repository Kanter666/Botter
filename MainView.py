import sys
from PyQt5 import uic, QtWidgets
import pyscreenshot as ImageGrab

qtViewFile = "./Design/Main.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.box = 0

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.start_button.clicked.connect(self.onclicked_start)

        self.stop_button.clicked.connect(self.onclicked_stop)

        self.fullsc_radb.setChecked(True)
        self.fullsc_radb.toggled.connect(self.full_screen_radb)
        self.boxsc_radb.toggled.connect(self.box_screen_radb)


    def onclicked_start(self):
        print("start", self.frequency_spin_box.value())
        if isinstance(self.box, int):
            im = ImageGrab.grab()
        else:
            im = ImageGrab.grab(self.box)
        im.show()

    def onclicked_stop(self):
        print("stop")

    def full_screen_radb(self):
        if self.fullsc_radb.isChecked():
            self.box = 0

    def box_screen_radb(self):
        if self.boxsc_radb.isChecked():
            self.box = [20, 20, 100, 100]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
