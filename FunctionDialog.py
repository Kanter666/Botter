from Models.BoxFunction import BoxFunction

import cv2
import numpy
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ImageViewerQt import ImageViewerQt
from PIL import Image, ImageFilter
from PIL.ImageQt import ImageQt


class FunctionDialog(QtWidgets.QDialog):
    def __init__(self, box, folder, current_view, function=None):
        super(FunctionDialog, self).__init__()
        uic.loadUi('./Design/BoxDialog.ui', self)
        self.filter_chb.setEnabled(False)
        self.threshold_hs.setEnabled(False)
        self.match_img_le.setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(lambda: self.done(1))
        self.function_type.buttonClicked.connect(self.function_selected)
        self.threshold_hs.valueChanged.connect(self.show_filter)
        self.box = box
        self.folder = folder
        self.match = None
        self.curren_view = current_view
        self.image_view = ImageViewerQt()
        self.match_img_le.mousePressEvent = self.get_match_image
        self.main_gl.addWidget(self.image_view, 7, 1, 2, 2)
        if function:
            self.name_le.setText(function.name)
            exec("self.{}_rb.setChecked(True)\n"
                 "self.function_selected(self.{}_rb)".format(function.type, function.type))
            if function.image:
                self.match = function.image
                self.match_img_le.setText(self.match)

    def get_function(self):
        text = self.get_radio_button()
        box_function = None
        if self.filter_chb.isChecked():
            threshold_value = self.threshold_hs.value()
        else:
            threshold_value = None
        if text == "Match img([] of x, y)":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "position", self.box, image=self.match)
        elif text == "Click()":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "click", self.box)
        elif text == "Get number(float)":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "number", self.box, threshold=threshold_value)
        elif text == "Get string(string)":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "string", self.box, threshold=threshold_value)

        return box_function

    def get_match_image(self, event):
        image, _ = QFileDialog.getOpenFileName(
            self,
            "Select file of image that you want to map",
            self.folder + "/Images",
            "Image Files (*.png)"
        )
        self.match = image
        self.match_img_le.setText(image)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)

    def show_filter(self):
        threshold = self.threshold_hs.value()
        print(threshold)
        exec("cropped = Image.open('{}').crop([{}, {}, {}, {}])\n"
             "im = cropped.filter(ImageFilter.EDGE_ENHANCE_MORE)\n"
             "npcropped = numpy.array(im)[:, :, ::-1].copy()\n"
             "npcropped = cv2.resize(npcropped, (0,0), fx=3, fy=3)\n"
             "im = Image.fromarray(npcropped)\n"
             "im = im.convert('L')\n"
             "im = im.point(lambda x: 0 if x<{} else 255, '1')\n"
             "self.image_view.setImage(QtGui.QPixmap.fromImage(ImageQt(im)))\n".format(self.curren_view,
                                int(self.box[0]), int(self.box[1]), int(self.box[0] + self.box[2]),
                                int(self.box[1] + self.box[3]),
                                threshold)
             )

    def get_radio_button(self):
        return self.function_type.checkedButton().text()

    def function_selected(self, btn):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        text = btn.text()
        if text == "Match img([] of x, y)" or text == "Click()":
            self.filter_chb.setEnabled(False)
            self.threshold_hs.setEnabled(False)
            if text == "Match img([] of x, y)":
                self.match_img_le.setEnabled(True)
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
            else:
                self.match_img_le.setEnabled(False)

        elif text == "Get number(float)" or text == "Get string(string)":
            self.filter_chb.setEnabled(True)
            self.threshold_hs.setEnabled(True)
            self.match_img_le.setEnabled(False)
