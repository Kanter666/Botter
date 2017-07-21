import sys

from PyQt5 import QtWidgets
from CreateView import CreateView
from StartView import StartView


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.central_widget = QtWidgets.QStackedWidget()
        self.setFixedSize(640, 640)
        self.setCentralWidget(self.central_widget)
        self.start_screen = StartView()
        self.create_screen = CreateView()
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.create_screen)
        self.central_widget.setCurrentWidget(self.start_screen)

        self.start_screen.clicked_create.connect(lambda: self.central_widget.setCurrentWidget(self.create_screen))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())