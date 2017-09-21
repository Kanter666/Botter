import sys

from PyQt5 import QtWidgets
from RecordView import CreateView
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
        self.resize(740, 500)
        self.start_screen = StartView()
        self.record_screen = CreateView()
        self.mapper_screen = ScreenMapperView()
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.record_screen)
        self.central_widget.addWidget(self.mapper_screen)
        self.central_widget.setCurrentWidget(self.start_screen)

        self.start_screen.clicked_record.connect(lambda: self.central_widget.setCurrentWidget(self.record_screen))
        self.start_screen.clicked_create.connect(self.open_mapper)
        self.start_screen.clicked_load.connect(self.load_library)
        self.record_screen.clicked_analyse.connect(self.open_mapper)
        self.mapper_screen.clicked_cancel.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))
        self.record_screen.clicked_cancel.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))

    def open_mapper(self):
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
        self.mapper_screen = ScreenMapperView()
        self.central_widget.addWidget(self.mapper_screen)
        self.central_widget.setCurrentWidget(self.mapper_screen)
        self.mapper_screen.set_arguments([arguments[0], arguments[1], arguments[3]], functions=arguments[2])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())