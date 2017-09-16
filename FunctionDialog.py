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
        self.get_text_widget = uic.loadUi('./Design/Get_text.ui')
        self.match_img_widget = uic.loadUi('./Design/Match_img.ui')

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(lambda: self.done(1))
        self.function_type.buttonClicked.connect(self.function_selected)
        self.get_text_widget.threshold_hs.valueChanged.connect(self.show_filter)
        self.match_img_widget.match_threshold_hs.valueChanged.connect(
            lambda: self.match_img_widget.threshold_lb.setText(
                "Match threshold : {} % ".format(self.match_img_widget.match_threshold_hs.value())
            )
        )
        self.box = box
        self.folder = folder
        self.match = None
        self.curren_view = current_view

        self.image_view = ImageViewerQt()

        self.match_img_widget.match_img_le.mousePressEvent = self.get_match_image
        self.get_text_widget.layout_gl.addWidget(self.image_view, 0, 1, 2, 2)

        self.additional_bl.addWidget(self.get_text_widget)
        self.additional_bl.addWidget(self.match_img_widget)
        self.get_text_widget.hide()
        self.match_img_widget.hide()
        if function:
            self.name_le.setText(function.name)
            if "image" in function.dictionary:
                self.match = function.dictionary["image"]
                self.match_img_widget.match_img_le.setText(self.match)
                self.match_img_widget.match_threshold_hs.setValue(function.dictionary["match_threshold"])
            elif "threshold" in function.dictionary:
                self.get_text_widget.threshold_hs.setValue(function.dictionary["threshold"])

            exec("self.{}_rb.setChecked(True)\n"
                 "self.function_selected(self.{}_rb)".format(function.type, function.type))

    def get_function(self):
        text = self.get_radio_button()
        box_function = None
        if self.get_text_widget.filter_chb.isChecked():
            threshold_value = self.get_text_widget.threshold_hs.value()
        else:
            threshold_value = None
        if text == "Match img([] of x, y)":
            box_function = BoxFunction(
                self.name_le.text().replace(" ", "_"), "position", self.box,
                {"image": self.match, "match_threshold": self.match_img_widget.match_threshold_hs.value()}
                )
        elif text == "Click()":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "click", self.box)
        elif text == "Get number(float)":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "number", self.box, {"threshold": threshold_value})
        elif text == "Get string(string)":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "string", self.box, {"threshold": threshold_value})
        elif text == "Has changed(bool)":
            box_function = BoxFunction(self.name_le.text().replace(" ", "_"), "change", self.box)

        return box_function

    def get_match_image(self, event):
        image, _ = QFileDialog.getOpenFileName(
            self,
            "Select file of image that you want to map",
            self.folder + "/Images",
            "Image Files (*.png)"
        )
        self.match = image
        self.match_img_widget.match_img_le.setText(image)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)

    def show_filter(self):
        threshold = self.get_text_widget.threshold_hs.value()
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
        self.get_text_widget.hide()
        self.match_img_widget.hide()
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        text = btn.text()
        if text == "Match img([] of x, y)":
            if not self.match_img_widget.match_img_le.text():
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
            self.match_img_widget.show()

        elif text == "Get number(float)" or text == "Get string(string)":
            self.get_text_widget.show()
