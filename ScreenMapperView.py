import os
import cv2
import sys
import importlib

from ImageViewerQt import ImageViewerQt
from FunctionDialog import FunctionDialog
from Models.Library import Library

from os import listdir
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QGraphicsRectItem


qtViewFile = "./Design/ScreenMapper.ui"

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class QCustomQWidget (QtWidgets.QWidget):
    def __init__ (self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.parent = parent
        self.qlist_widget = None
        self.name_l = QtWidgets.QLabel()
        self.name_l.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.all_layout = QtWidgets.QHBoxLayout()
        self.run_bt = QtWidgets.QPushButton()
        self.run_bt.setIcon(QtGui.QIcon("./img/play_bt.png"))
        self.edit_bt = QtWidgets.QPushButton()
        self.edit_bt.setIcon(QtGui.QIcon("./img/edit_bt.png"))
        self.delete_bt = QtWidgets.QPushButton()
        self.delete_bt.setIcon(QtGui.QIcon("./img/delete_bt.png"))
        self.run_bt.clicked.connect(self.set_selected)
        self.edit_bt.clicked.connect(self.set_selected)
        self.delete_bt.clicked.connect(self.set_selected)
        self.run_bt.clicked.connect(self.parent.run_function_press)
        self.edit_bt.clicked.connect(self.parent.edit_function_press)
        self.delete_bt.clicked.connect(self.parent.delete_function_press)
        self.all_layout.addWidget(self.name_l, 70)
        self.all_layout.addWidget(self.run_bt, 10)
        self.all_layout.addWidget(self.edit_bt, 10)
        self.all_layout.addWidget(self.delete_bt, 10)

        self.setLayout(self.all_layout)

    def setName(self, text):
        self.name_l.setText(text)

    def set_widget(self, widget):
        self.qlist_widget = widget

    def set_selected(self):
        self.parent.box_function_lw.setCurrentRow(self.parent.box_function_lw.indexFromItem(self.qlist_widget).row())


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
        self.position_img = None

        self.rename_lib_ml.triggered.connect(self.change_name_press)
        self.screenshots_folder_ml.triggered.connect(self.switch_function_press)

        self.cancel_bt.clicked.connect(self.clicked_cancel.emit)
        self.save_image_bt.clicked.connect(self.save_image_press)
        self.add_function_bt.clicked.connect(self.add_function_press)
        self.screens_cb.currentIndexChanged.connect(self.screen_changed)
        self.box_function_lw.itemSelectionChanged.connect(self.show_box)
        self.position_img_bt.clicked.connect(self.position_from_image)

        self.name_l.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))

        self.image_view = ImageViewerQt()
        self.grid_layout.addWidget(self.image_view, 0, 0, 35, 1)
        self.grid_layout.setColumnStretch(0, 99)

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
        if len(arguments) > 2:
            if "position_image" in arguments[2]:
                self.position_img = arguments[2]["position_image"]
                self.position_img_bt.setText("Position image is set")
        self.name_l.setText(self.library)
        self.box_functions = functions
        for fun in functions:
            self.add_function(fun)
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

    def position_from_image(self):
            box = self.image_view.getBoxDimensions()
            img = cv2.imread(self.folder + "/" + self.screens_cb.currentText())

            imCrop = img[int(box[1]):int(box[1] + box[3]), int(box[0]):int(box[0] + box[2])]

            if not os.path.exists(self.folder + "/Images"):
                os.makedirs(self.folder + "/Images")

            cv2.imwrite(self.folder+"/Images/position_img.png", imCrop)
            self.position_img = [int(box[0]),int(box[1])]
            self.position_img_lb.setText("Position image is set")

            self.create_lib()

    def save_image_press(self):

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

    def add_function_press(self):
        box = self.image_view.getBoxDimensions()

        if box:
            dialog = FunctionDialog(box, self.folder, (self.folder+"/"+self.screens_cb.currentText()))
            if dialog.exec_():
                function_box = dialog.get_function()
                self.box_functions.append(function_box)
                self.add_function(function_box)
                self.create_lib()

    def edit_function_press(self):

        index = self.box_function_lw.currentRow()
        box = self.box_functions[index].box

        dialog = FunctionDialog(
            box, self.folder, (self.folder+"/"+self.screens_cb.currentText()), function=self.box_functions[index]
        )
        if dialog.exec_():
            function_box = dialog.get_function()
            self.delete_function_press()
            self.box_functions.append(function_box)
            self.add_function(function_box)
            self.create_lib()

    def add_function(self, function):

        # Create QCustomQWidget
        myQCustomQWidget = QCustomQWidget(self)
        myQCustomQWidget.setName("{}({})".format(function.name, function.type))
        # Create QListWidgetItem
        myQListWidgetItem = QtWidgets.QListWidgetItem(self.box_function_lw)
        # Set size hintItem(myQListWidgetItem)
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

        myQCustomQWidget.set_widget(myQListWidgetItem)

        # Add QListWidgetItem into QListWidget
        self.box_function_lw.addItem(myQListWidgetItem)
        self.box_function_lw.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def delete_function_press(self):
        index = self.box_function_lw.currentRow()
        print("Current inde is {}, and name of the function should be: {}".format(index, self.box_functions[index].name))
        self.box_function_lw.takeItem(index)
        del self.box_functions[index]
        self.create_lib()

    def run_function_press(self):
        index = self.box_function_lw.currentRow()
        if index > -1:
            function = self.box_functions[index]
            lib = os.path.basename(os.path.normpath(self.library))

            if function.type == "game_box":
                if self.image_view.current_box:
                    self.image_view.scene.removeItem(self.image_view.current_box)
                self.image_view.box_dimension = function.box
                self.image_view.current_box = QGraphicsRectItem(
                    function.box[0], function.box[1], function.box[2], function.box[3]
                )
                self.image_view.current_box.setPen(self.image_view.box_style)
                self.image_view.scene.addItem(self.image_view.current_box)

            elif function.type == "change" or function.type == "click":
                QMessageBox.about(self, 'Run function', 'Function {} from class {} can not be runned in this enviroment'.format(function.name, lib))
            else:
                print("sys.path.append('{}')\n"
                     "import {}\n"
                     "importlib.reload({})\n"
                     "print('library imported')\n"
                     "library = {}.{}()\n"
                     "library.grab_file('{}')\n"
                     "result = library.{}()\n"
                     "QMessageBox.about(self, 'Run function', 'Function {} from class {} returns '+str(result))".format(
                        self.library[:-len(lib)],
                        lib[:-3], lib[:-3], lib[:-3], lib[:-3],
                        (self.folder+"/"+self.screens_cb.currentText()),
                        self.box_functions[index].name,
                        self.box_functions[index].name, lib)
                        )
                exec("sys.path.append('{}')\n"
                     "import {}\n"
                     "importlib.reload({})\n"
                     "print('library imported')\n"
                     "library = {}.{}()\n"
                     "library.grab_file('{}')\n"
                     "result = library.{}()\n"
                     "QMessageBox.about(self, 'Run function', 'Function {} from class {} returns '+str(result))".format(
                        self.library[:-len(lib)],
                        lib[:-3], lib[:-3], lib[:-3], lib[:-3],
                        (self.folder+"/"+self.screens_cb.currentText()),
                        self.box_functions[index].name,
                        self.box_functions[index].name, lib)
                        )

    def switch_function_press(self):

        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        files = [file for file in listdir(self.folder) if file[-4:] == ".png"]
        self.screens_cb.clear()
        self.screens_cb.addItems(files)
        self.screens_cb.setCurrentIndex(0)
        if os.path.isfile(self.folder + "/box.txt"):
            with open(self.folder + "/box.txt", 'r') as f:
                self.box = eval(f.readline())

    def show_box(self):
        box = self.box_functions[self.box_function_lw.currentRow()].box
        self.image_view.show_selected_box(box)

    def change_name_press(self):
        directory, _ = QFileDialog.getSaveFileName(
            self,
            "Create library file",
            self.folder,
            "Python Files (*.py)"
        )
        if directory[-3:] != ".py":
            directory += ".py"
        if os.path.exists(self.library):
            os.remove(self.library)
        self.library = directory
        self.name_l.setText(self.library)
        self.create_lib()

    def create_lib(self):
        Library.create_library(
            self.library,
            self.box,
            self.folder,
            self.box_functions,
            {"position_image": self.position_img}
        )

