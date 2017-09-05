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
        self.setCentralWidget(self.central_widget)
        self.resize(640, 480)
        self.start_screen = StartView()
        self.create_screen = CreateView()
        self.mapper_screen = ScreenMapperView()
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.create_screen)
        self.central_widget.addWidget(self.mapper_screen)
        self.central_widget.setCurrentWidget(self.start_screen)

        self.start_screen.clicked_create.connect(lambda: self.central_widget.setCurrentWidget(self.create_screen))
        self.start_screen.clicked_load.connect(self.load_library)
        self.create_screen.clicked_analyse.connect(self.openMapper)
        self.mapper_screen.clicked_cancel.connect(lambda: self.central_widget.setCurrentWidget(self.create_screen))

    def openMapper(self, arguments):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory with your screen recording"))
        directory, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Create library file",
            ".",
            "Python Files (*.py)"
        )
        if directory[-3:] != ".py":
            directory += ".py"
        self.central_widget.setCurrentWidget(self.mapper_screen)
        self.mapper_screen.set_arguments([file, directory])

    def load_library(self, arguments):
        self.central_widget.setCurrentWidget(self.mapper_screen)
        self.mapper_screen.set_arguments([arguments[0], arguments[1]], functions=arguments[2])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())