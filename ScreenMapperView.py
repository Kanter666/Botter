import os
import cv2
import sys

from ImageViewerQt import ImageViewerQt
from FunctionDialog import FunctionDialog
from Models.Library import Library

from os import listdir
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox

qtViewFile = "./Design/ScreenMapper.ui"  # Enter file here.

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class ScreenMapperView(QtWidgets.QMainWindow, Ui_StartWindow):

    clicked_cancel = pyqtSignal()

    def __init__(self):

        self.folder = None
        self.library = None

        QtWidgets.QMainWindow.__init__(self)
        Ui_StartWindow.__init__(self)
        self.setupUi(self)

        self.box_functions = []
        self.box = None

        self.cancel_bt.clicked.connect(self.clicked_cancel.emit)
        self.change_name_bt.clicked.connect(self.change_name)
        self.save_image_bt.clicked.connect(self.save_image)
        self.add_function_bt.clicked.connect(self.add_function)
        self.delete_bt.clicked.connect(self.delete_function)
        self.run_bt.clicked.connect(self.run_function)
        self.screens_cb.currentIndexChanged.connect(self.screen_changed)
        self.box_function_lw.itemSelectionChanged.connect(self.show_box)

        self.image_view = ImageViewerQt()
        self.grid_layout.addWidget(self.image_view, 0, 0, 10, 1)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtWidgets.qApp.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            print(event.key())
        return super(ScreenMapperView, self).eventFilter(source, event)

    def handleFullScreen(self):
        if self.central_widget.isFullScreen():
            print("Setting to normal")
            self.central_widget.showMaximized()
        else:
            print("Setting to max")
            self.central_widget.showFullScreen()

    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)

    def set_arguments(self, arguments, functions=[]):
        self.folder = arguments[0]
        self.library = arguments[1]
        self.box_functions = functions
        for fun in functions:
            self.box_function_lw.addItem("{}({})".format(fun.name, fun.type))
        files = [file for file in listdir(self.folder) if file[-4:] == ".png"]
        self.screens_cb.clear()
        self.screens_cb.addItems(files)
        self.screens_cb.setCurrentIndex(0)
        if os.path.isfile(self.folder + "/box.txt"):
            with open(self.folder + "/box.txt", 'r') as f:
                self.box = eval(f.readline())

    def screen_changed(self, i):
        image = self.folder+"/"+self.screens_cb.currentText()
        self.image_view.loadImageFromFile(image)
        print(self.folder+"/"+self.screens_cb.currentText())

    # A key has been pressed!
    def keyPressEvent(self, event):
        print("Key pressed: ")
        print(event.key())
        # key up
        if event.key() == 16777235:
            if self.screens_cb.currentIndex() > 0:
                self.screens_cb.setCurrentIndex(self.screens_cb.currentIndex() - 1)
        # key down
        elif event.key() == 16777237:
            if self.screens_cb.currentIndex() < (self.screens_cb.count() - 1):
                self.screens_cb.setCurrentIndex(self.screens_cb.currentIndex() + 1)

    def save_image(self):

        box = self.image_view.getBoxDimensions()
        img = cv2.imread(self.folder+"/"+self.screens_cb.currentText())

        imCrop = img[int(box[1]):int(box[1] + box[3]), int(box[0]):int(box[0] + box[2])]

        if not os.path.exists(self.folder+"/Images"):
            os.makedirs(self.folder+"/Images")

        directory, _ = QFileDialog.getSaveFileName(
            self,
            "Save image",
            self.folder+"/Images",
            "Image Files (*.png)"
        )
        cv2.imwrite(directory+".png", imCrop)

    def add_function(self):
        box = self.image_view.getBoxDimensions()

        if box:
            dialog = FunctionDialog(box, self.folder, (self.folder+"/"+self.screens_cb.currentText()))
            dialog.exec_()
            if dialog.result() == 0:
                function_box = dialog.get_function()
                print("got function")
                self.box_functions.append(function_box)
                self.box_function_lw.addItem("{}({})".format(function_box.name, function_box.type))
                Library.create_library(self.library, self.box, self.folder, self.box_functions)

    def delete_function(self):
        index = self.box_function_lw.currentRow()
        print("Current inde is {}, and name of the function should be: {}".format(index, self.box_functions[index].name))
        self.box_function_lw.takeItem(index)
        del self.box_functions[index]
        Library.create_library(self.library, self.box, self.folder, self.box_functions)

    def run_function(self):
        index = self.box_function_lw.currentRow()
        if index > -1:
            lib = os.path.basename(os.path.normpath(self.library))
            print("sys.path.append('{}')\n"
                  "from {} import {} as testlib\n"
                  "print('library imported')\n"
                  "library = testlib()\n"
                  "print(library.{}())".format(self.library[:-len(lib)], lib[:-3], lib[:-3],  self.box_functions[index].name)
                  )
            exec("sys.path.append('{}')\n"
                  "from {} import {} as testlib\n"
                  "print('library imported')\n"
                  "library = testlib()\n"
                  "result = library.{}()\n"
                 "QMessageBox.about(self, 'Run function', 'Function {} from class {} returns '+str(result))".format(
                self.library[:-len(lib)], lib[:-3], lib[:-3],  self.box_functions[index].name, self.box_functions[index].name, lib)
                  )

    def show_box(self):
        box = self.box_functions[self.box_function_lw.currentRow()].box
        self.image_view.show_selected_box(box)

    def change_name(self):
        directory, _ = QFileDialog.getSaveFileName(
            self,
            "Create library file",
            self.folder,
            "Python Files (*.py)"
        )
        if os.path.exists(self.library):
            os.remove(self.library)
        self.library = directory
        Library.create_library(self.library, self.box, self.folder, self.box_functions)

