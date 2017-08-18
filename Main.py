import sys

from PyQt5 import QtWidgets
from CreateView import CreateView
from StartView import StartView
from ScreenMapperView import ScreenMapperView


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.central_widget = QtWidgets.QStackedWidget()
        self.setFixedSize(800, 600)
        self.setCentralWidget(self.central_widget)
        self.start_screen = StartView()
        self.create_screen = CreateView()
        self.mapper_screen = ScreenMapperView()
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.create_screen)
        self.central_widget.addWidget(self.mapper_screen)
        self.central_widget.setCurrentWidget(self.start_screen)

        self.start_screen.clicked_create.connect(lambda: self.central_widget.setCurrentWidget(self.create_screen))
        self.create_screen.clicked_analyse.connect(self.openMapper)
        self.mapper_screen.clicked_cancel.connect(lambda: self.central_widget.setCurrentWidget(self.create_screen))

    def openMapper(self, arguments):
        self.central_widget.setCurrentWidget(self.mapper_screen)
        self.mapper_screen.set_arguments(arguments)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())