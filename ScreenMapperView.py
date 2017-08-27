import os
import cv2

from ImageViewerQt import ImageViewerQt
from FunctionDialog import FunctionDialog
from os import listdir
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QDialog

qtViewFile = "./Design/ScreenMapper.ui"  # Enter file here.

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class ScreenMapperView(QtWidgets.QMainWindow, Ui_StartWindow):

    clicked_cancel = pyqtSignal()

    def __init__(self):

        self.folder = None

        QtWidgets.QMainWindow.__init__(self)
        Ui_StartWindow.__init__(self)
        self.setupUi(self)

        self.cancel_bt.clicked.connect(self.clicked_cancel.emit)
        self.finish_bt.clicked.connect(self.print_arguments)
        self.save_image_bt.clicked.connect(self.save_image)
        self.add_function_bt.clicked.connect(self.add_function)
        self.screens_cb.currentIndexChanged.connect(self.screen_changed)

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

    def set_arguments(self, arguments):
        self.folder = arguments[0]
        files = listdir(self.folder)
        self.screens_cb.clear()
        self.screens_cb.addItems(files)
        self.screens_cb.setCurrentIndex(0)

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
            name = FunctionDialog.get_function()
            print("Got this name: "+name)

    def print_arguments(self):
        print(self.text)
